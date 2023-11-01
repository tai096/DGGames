from flask import Blueprint, render_template, flash, request, jsonify, redirect
import os
import datetime
import cv2
import face_recognition
from utils.tools import MessageType
from models import registered_faces
from app import db


auth_blueprint = Blueprint('auth', __name__, template_folder='templates')
registered_data = {}

@auth_blueprint.route('/register')
def register():
    return render_template('register.html')

@auth_blueprint.route('/login')
def login():

    return render_template('login.html')

@auth_blueprint.route('/face-id-register')
def face_id_register_ui():
    return render_template('face-id-register.html')

@auth_blueprint.route('/face-id-login')
def face_id_login_ui():
    return render_template('face-id-login.html')

@auth_blueprint.route('/register-face-id', methods=["POST"])
def register_face_id():
    name = request.form.get("name")
    photo = request.form.get("photo")
    
    new_user = registered_faces(username = name, photo = photo)

    try:
        db.session.add(new_user)
        db.session.commit()

        success_message = "Signed up successfully!"
        flash(f'{success_message}', category = MessageType['SUCCESS'].value)
    except:
        error_message = "Something went wrong! (POST: auth/register-face-id)"
        flash(f'Error: {error_message}', category = MessageType['ERROR'].value)

        db.session.rollback()
        
    finally:
        return redirect('/auth/login')
    



