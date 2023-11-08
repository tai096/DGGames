from flask import Blueprint, render_template, request, redirect, session, flash, get_flashed_messages, url_for
import sqlite3, bcrypt, re

auth_blueprint = Blueprint('auth', __name__, template_folder='templates', static_folder='static')
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
    role = "customer"
    budget = "0"
    id_max = generateID()
    if id_max > 0:
        id_max += 1
    else: id_max = 1
    conn = sqlite3.connect(sqldbname, timeout=30)
    cursor = conn.cursor()
    sqlcommand = (f'Insert Into user (id, name, username, email, hash_password, phone_number, role, budget) VALUES ({id_max}, "{name}", "{username}", "{email}", "{hashed_password}", "{phone_number}", "{role}", "{budget}")')
    cursor.execute(sqlcommand)
    conn.commit()
    conn.close()
    return id_max

def get_obj_user(email):
    result = []
    conn = sqlite3.connect(sqldbname, timeout=30)
    cursor = conn.cursor()
    sqlcommand = (f'Select * from user where email = "{email}"')
    cursor.execute(sqlcommand)
    obj_user = cursor.fetchone()
    if obj_user != None:
        result = obj_user
    else:
        result = [0, 0, 0, 0]
    conn.close()
    return result

def validate_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False

def validate_number(phone):
    if phone.isnumeric():
        return True
    return False

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        phone_error = ""
        username_error = ""
        email_error = ""
        if validate_number(phone) == False:
            phone_error = "*Invalid Phone Number!"
            return render_template('register.html', phone_error=phone_error)
        if validate_email(email) == False:
            email_error = "*Invalid Email Address!"
            return render_template('register.html', email_error=email_error)
        if check_notunique_username(username) or check_notunique_email(email):
            if check_notunique_username(username):
                username_error = "*Username already exists!"
            if check_notunique_email(email):
                email_error = "*Email already exists!"
            return render_template('register.html', username_error=username_error, email_error=email_error, 
                           registration_success="")
        hash = password.encode('utf-8')
        hashed_password_bytes = bcrypt.hashpw(hash, bcrypt.gensalt())
        hashed_password_str = hashed_password_bytes.decode()
        new_id = save_to_db(name, username, email, hashed_password_str, phone)
        return redirect(url_for('auth.login'))
    return render_template('register.html', username_error="", email_error="")

@auth_blueprint.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        obj_user = get_obj_user(email)
        if int(obj_user[0]) > 0:
            obj_pw = obj_user[3]
            obj_pw_encoded = obj_pw.encode('utf-8')
            check_hash = bcrypt.checkpw(password.encode('utf-8'), obj_pw_encoded)
            if check_hash == True:
                curr_user = {
                    "id": obj_user[0],
                    "username": obj_user[1],
                    "name": obj_user[5],
                    "phone_number": obj_user[6],
                    "budget": obj_user[7]
                }
                session['current_user'] = curr_user
                return redirect(url_for('general.index'))
            else:
                login_error = "*Invalid email or password!"
                return render_template('login.html', login_error=login_error)
        else:
            login_error = "*Invalid email or password!"
            return render_template('login.html', login_error=login_error)
    return render_template('login.html', login_error="")