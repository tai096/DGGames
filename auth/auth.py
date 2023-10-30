from flask import Blueprint, render_template, flash, request, jsonify
import os
import datetime
import cv2
import face_recognition
from utils.tools import MessageType


auth_blueprint = Blueprint('auth', __name__, template_folder='templates')
registered_data = {}

@auth_blueprint.route('/register')
def register():
    return render_template('register.html')

@auth_blueprint.route('/login')
def login():

    return render_template('login.html')

@auth_blueprint.route('/face-id')
def face_id():
    return render_template('face-id.html')

@auth_blueprint.route('/register-face-id', methods=["POST"])
def register_face_id():
    name = request.form.get("name")
    photo = request.files['photo']

    # save photo to upload_folder
    upload_folder = os.path.join(os.getcwd(), "static", "uploads")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    photo.save(os.path.join(upload_folder,f'{datetime.date.today()}'))

    registered_data[name] = f'{datetime.date.today()}.jpg'
    
    success_message = "Signed up successfully!"
    flash(f'{success_message}', category = MessageType['SUCCESS'].value)

    response = {'success':True, 'name': name}
    return jsonify(response)

# @auth_blueprint.route('/login-face-id', methods=["POST"])
# def login_face_id():
#     photo = request.files['photo']

#     # save photo to upload_folder
#     upload_folder = os.path.join(os.getcwd(), "static", "uploads")
#     if not os.path.exists(upload_folder):
#         os.makedirs(upload_folder)
    
#     login_photo_filename = os.path.join(upload_folder,'login_face.jpg')

#     photo.save(login_photo_filename)

#     # detect face
#     login_photo = cv2.imread(login_photo_filename)
#     gray_image = cv2.cvtColor(login_photo, cv2.COLOR_GRAY2BGR)

#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     faces = face_cascade.detectMultiScale(gray_image, scaleFactor = 1.1, minNeighbors = 5, minSize = (30,30))

#     if len(faces) == 0:
#         error_message = "Something went wrong! (POST: auth/login-face-id)"
#         flash(f'Error: {error_message}', category = MessageType['ERROR'].value)
#     else:
#         login_photo = face_recognition.load_image_file(login_photo_filename)

#         login_face_encodings = face_recognition.face_encodings(login_photo)

#         for name, filename in registered_data.items():
#             registered_photo = os.path.join(upload_folder, filename)
#             registered_image = face_recognition.load_image_file(registered_photo)

#             registered_face_encodings = face_recognition.face_encodings(registered_image)

#             if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
#                 matches = face_recognition.compare_faces(registered_face_encodings,login_face_encodings[0])
            
#             print("matches: ", matches)
#             if any(matches):
#                 success_message = "Logged in successfully!"
#                 flash(f'{success_message}', category = MessageType['SUCCESS'].value)

@auth_blueprint.route('/login-face-id', methods=["POST"])
def login_face_id():
    photo = request.files['photo']

    # save photo to upload_folder
    upload_folder = os.path.join(os.getcwd(), "static", "uploads")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    login_photo_filename = os.path.join(upload_folder, 'login_face.jpg')

    photo.save(login_photo_filename)

    # detect face
    login_photo = cv2.imread(login_photo_filename)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(login_photo, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    print(login_photo)

    if len(faces) == 0:
        error_message = "Something went wrong! (POST: auth/login-face-id)"
        flash(f'Error: {error_message}', category=MessageType['ERROR'].value)

        return jsonify({"success": False})
    
    login_photo = face_recognition.load_image_file(login_photo_filename)

    login_face_encodings = face_recognition.face_encodings(login_photo)

    for name, filename in registered_data.items():
        registered_photo = os.path.join(upload_folder, filename)
        registered_image = face_recognition.load_image_file(registered_photo)

        registered_face_encodings = face_recognition.face_encodings(registered_image)

        if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
            matches = face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])
            

            if any(matches):
                success_message = "Logged in successfully!"
                flash(f'{success_message}', category=MessageType['SUCCESS'].value)
                
                print("matches: ", matches)
                
                return jsonify({"success": True})
    
    return jsonify({"success": False})
