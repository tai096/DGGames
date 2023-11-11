from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from utils.tools import MessageType
from app import db
from models import Games, Publisher, Genre, Platform

user_blueprint = Blueprint('user', __name__, template_folder='templates')

@user_blueprint.route('/profile')
def profile():
    if 'current_user' in session:

        
        return render_template('profile.html')
        
    else:
        return redirect(url_for('auth.login'))

@user_blueprint.route('/my-wallet')
def wallet():
    if 'current_user' in session:

        
        return render_template('wallet.html')
        
    else:
        return redirect(url_for('auth.login'))