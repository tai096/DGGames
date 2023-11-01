from flask import Blueprint, render_template, request, redirect, session, flash, get_flashed_messages, url_for
import sqlite3
from flask_bcrypt import Bcrypt

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')
sqldbname = 'instance/dggames.db'

def generateID():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sqlcommand = "SELECT Max(id) from user"
    cursor.execute(sqlcommand)
    max_id = cursor.fetchone()[0]
    return max_id;

def check_notunique_email(email):
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sql_command = (f'Select * from user where email = "{email}"')
    cursor.execute(sql_command)
    data = cursor.fetchall()
    conn.close()
    return data

def check_notunique_username(username):
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sql_command = (f'Select * from user where name = "{username}"')
    cursor.execute(sql_command)
    data = cursor.fetchall()
    conn.close()
    return data

def save_to_db(name, username, email, hashed_password, phone_number):
    id_max = generateID()
    if id_max > 0:
        id_max += 1
    else: id_max = 1
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sqlcommand = (f'Insert Into user (id, name, username, email, password, phone_number) VALUES ({id_max}, "{name}", "{username}", "{email}", "{hashed_password}", "{phone_number}")')
    cursor.execute(sqlcommand)
    conn.commit()
    conn.close()
    return id_max

def get_obj_user(username, hashed_password):
    result = []
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sqlcommand = (f'Select * from user where name = "{username}" and password= "{hashed_password}"')
    cursor.execute(sqlcommand)
    obj_user = cursor.fetchone()
    if len(obj_user) > 0:
        result = obj_user
    conn.close()
    return result

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        username_error = ""
        email_error = ""
        registration_success = ""
        if check_notunique_username(username) or check_notunique_email(email):
            if check_notunique_username(username):
                username_error = "Username already exists!"
            if check_notunique_email(email):
                email_error = "Email already exists!"
            return render_template('register.html', username_error=username_error, email_error=email_error, 
                           registration_success="")
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
        new_id = save_to_db(name, username, email, hashed_password, phone)
        flash(f'Register Successfully, ID = {new_id}', category='success')
        return redirect(url_for('login'))

    return render_template('register.html', username_error="", email_error="", 
                           registration_success="")

@auth_blueprint.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        obj_user = get_obj_user(username, hashed_password)

        if int(obj_user[0]) > 0:
            curr_user = {
                "id": obj_user[0],
                "name": obj_user[1],
                "email": obj_user[2]
            }
            session['current_user'] = curr_user
            return redirect(url_for('index'))
        else:
            flash("Username and password are not correct!", category='danger')
    return render_template('login.html')