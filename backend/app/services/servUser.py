from app.model.user import User, check_password_hash
from .servDb import getAll, register, getUserUsername, getUserMail
from flask import jsonify, make_response
import uuid
import re
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, DynamicTemplateData

SENDGRID_API_KEY = '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'

def registerUser(username, password, email):
    if getUserUsername(username):
        return jsonify({"success": False, "message": "Username already exists"}), 409
    user =User(username=username, email=email)
    user.hashPassword(password)
    user.id = str(uuid.uuid4())
    try:
        register(user.id,user.username, user.passwordHash, user.email)
        response = make_response(jsonify({"success":True, "message": "You are now registred, make your profile!"}))
        tempId = str(uuid.uuid4)
        response.set_cookie(
                "userId",
                user.id, 
                httponly=True, 
                secure=False, 
                samesite="None", 
                max_age=60*60*24     # 1dan
        )
        response.status_code = 200
        return response
    except:
        return jsonify({"success":False, "message": "There was an error, please try again."}), 400


def loginUser(identifier, password):
    EMAILPATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(EMAILPATTERN, identifier):
        uporabnik = getUserMail(identifier)
        if not uporabnik:
            return jsonify({"success": False, "message": "Account does not exist, please register!"}), 404
        
        userId = uporabnik["userId"]
        if check_password_hash(uporabnik["hashPass"],password) == True:
            response = make_response(jsonify({"success":True, "message":"You are logged in!"}))
            response.set_cookie(
                "sessionId",
                userId, 
                httponly=True, 
                secure=False, 
                samesite="None", 
                max_age=60*60*24     # 1 dan
            )
            response.status_code = 200
            return response
        else:
            return jsonify({"success": False, "message": "Wrong password"}), 401
    else:
        uporabnik = getUserUsername(identifier)
        if not uporabnik:
            return jsonify({"success": False, "message": "Account does not exist, please register!"}), 404
        userId = uporabnik["userId"]
        if check_password_hash(uporabnik["hashPass"],password):
            response = make_response(jsonify({"success":True, "message":"You are logged in!"}))
            response.set_cookie(
                "sessionId",
                userId, 
                httponly=True, 
                secure=False, 
                samesite="None", 
                max_age=60*60*24     # 1 day expiration
            )
            response.status_code = 200
            return response
        else:
            return jsonify({"success": False, "message": "Napačno geslo"}), 401

def forgotPass(email, link):
    message = Mail(
    from_email='cmi.city.eu@gmail.com', 
    to_emails=email,
    )
    message.template_id = 'd-a2cf4800999b4d3b9ab3f8c62e511206'
    message.dynamic_template_data = {
    'link': link
    }

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f'Status code: {response.status_code}')
    except:
        print(f'Status code: {response.status_code}')