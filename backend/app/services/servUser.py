from app.model.user import User, check_password_hash
from .servAuthDb import getAll, register, getUserUsername, getUserMail, checkAdmin, addAdminDb
from flask import jsonify, make_response
import uuid
import re
import os

def registerUser(username, password, email):
    if getUserUsername(username):
        return jsonify({"success": False, "message": "Username already exists"}), 409
    user =User(username=username, email=email)
    user.hashPassword(password)
    user.id = str(uuid.uuid4())
    try:
        register(user.id,user.username, user.passwordHash, user.email)
        response = make_response(jsonify({"success":True, "message": "You are now registred, make your profile!"}))
        response.set_cookie(
                "sessionId",
                user.id, 
                httponly=False, 
                secure=False, 
                samesite="Lax", 
                max_age=60*60*24     # 1dan
        )
        response.status_code = 200
        return response
    except:
        return jsonify({"success":False, "message": "There was an error, please try again."}), 400


def loginUser(identifier, password, remember):
    print(remember)
    EMAILPATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(EMAILPATTERN, identifier):
        uporabnik = getUserMail(identifier)
        if not uporabnik:
            return jsonify({"success": False, "message": "Account does not exist, please register!"}), 404
        
        userId = uporabnik["userId"]
        if check_password_hash(uporabnik["hashPass"],password) == True:
            response = make_response(jsonify({"success":True, "message":"You are logged in!"}))
            if remember == True:
                response.set_cookie(
                    "sessionId",
                    userId, 
                    httponly=False, 
                    secure=False, 
                    samesite="Lax", 
                    max_age=60*60*24*30     # 1 mesec
                )
                response.status_code = 200
                return response
            else:
                response.set_cookie(
                    "sessionId",
                    userId, 
                    httponly=False, 
                    secure=False, 
                    samesite="Lax", 
                )
                response.status_code = 200
                return response
        else:
            return jsonify({"success": False, "message": "Wrong password"}), 401
    else:
        uporabnik = getUserUsername(identifier)
        if not uporabnik:
            print("if not uporabnik")
            return jsonify({"success": False, "message": "Account does not exist, please register!"}), 404
        userId = uporabnik["userId"]
        if check_password_hash(uporabnik["hashPass"],password):
            print("if chech pass hash")
            response = make_response(jsonify({"success":True, "message":"You are logged in!"}))
            if remember == True:
                response.set_cookie(
                    "sessionId",
                    userId, 
                    httponly=False, 
                    secure=False, 
                    samesite="Lax", 
                    max_age=60*60*24*30     # 1 mesec
                )
                response.status_code = 200
                return response
            else:
                response.set_cookie(
                    "sessionId",
                    userId, 
                    httponly=False, 
                    secure=False, 
                    samesite="Lax", 
                )
                response.status_code = 200
                return response
        else:
            print("napačno geslo")
            return jsonify({"success": False, "message": "Napačno geslo"}), 401

def addAdmin(userId):
    if checkAdmin(userId) ==False:
        addAdminDb(userId)
        return True
    else:
        return False

        
        