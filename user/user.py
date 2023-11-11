from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from utils.tools import MessageType
from app import db
from models import User
import bcrypt

user_blueprint = Blueprint('user', __name__, template_folder='templates')

@user_blueprint.route('/profile')
def profile():
    if 'current_user' in session:

        
        return render_template('profile.html')
        
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