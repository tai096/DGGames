from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from utils.tools import MessageType
from app import db
from models import User
import bcrypt

user_blueprint = Blueprint('user', __name__, template_folder='templates')

@user_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'current_user' in session:
        curr_user = session['current_user']
        user_query = User.query.filter_by(id = curr_user['id']).first()
        
        return render_template('profile.html', user_query = user_query)
        
    else:
        return redirect(url_for('auth.login'))

@user_blueprint.route('/profile/update', methods=['POST'])

def update_profile():
    if 'current_user' in session:
        curr_user = session['current_user']

        user_query = User.query.filter_by(id = curr_user['id']).first()

        email = request.form['email']
        username = request.form['username']
        name = request.form['name']
        phone = request.form['phone']
        avatar = request.form['avatar']

        try:
            user_query.email = email
            user_query.username = username
            user_query.name = name
            user_query.phone_number = phone
            user_query.avatar = avatar

            db.session.commit()

            session['current_user']['email'] = user_query.email
            session['current_user']['username'] = user_query.username
            session['current_user']['name'] = user_query.name
            session['current_user']['phone_number'] = user_query.phone_number

            success_message = "Updated successfully!"
            flash(f'{success_message}', category = MessageType['SUCCESS'].value)

        except:
            error_message = "Something went wrong at POST: /profile"
            flash(f'Error: {error_message}', category = MessageType['ERROR'].value)
        
        return redirect(url_for('user.profile'))
        
    else:
        return redirect(url_for('auth.login'))

@user_blueprint.route('/my-wallet', methods=['GET', 'POST'])
def wallet():
    if 'current_user' in session:
        curr_user = session['current_user']

        user_query = User.query.filter_by(id = curr_user['id']).first()


        if request.method == "POST":
            top_up_value = request.form['top_up']
            password = request.form['password']
            encoded_pass = user_query.hash_password.encode('utf-8')

            check_hash = bcrypt.checkpw(password.encode('utf-8'), encoded_pass)

            if check_hash == True:
                user_query.budget = user_query.budget + int(top_up_value)
                db.session.commit()

                session['current_user']['budget'] = user_query.budget

                success_message = "Top Up successfully!"
                flash(f'{success_message}', category = MessageType['SUCCESS'].value)
    
            else:
                error_message = "Incorrect password!"
                flash(f'Error: {error_message}', category = MessageType['ERROR'].value)
        
        return render_template('wallet.html', user_query = user_query)
    else:
        return redirect(url_for('auth.login'))