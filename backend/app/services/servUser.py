from app.model.user import User, check_password_hash
from .servDb import getAll, register, getUserUsername, getUserMail
from flask import jsonify, make_response
import uuid
import re

def registerUser(username, password, email):
    users = getAll("uporabniki")
    if getUserUsername(username):
        return
    user =User(username=username, email=email)
    user.hashPassword(password)
    user.id = str(uuid.uuid4())
    register(user.id,user.username, user.passwordHash, user.email)

def loginUser(identifier, password):
    emailPattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(emailPattern, identifier):
        uporabnik = getUserMail(identifier)
        if not uporabnik:
            return jsonify({"success": False, "message": "račun ne obstaja"})
        userId = uporabnik["userId"]
        if check_password_hash(uporabnik["hashPass"],password):
            response = make_response(jsonify({"success":True, "message":"Login uspešen"}))
            response.set_cookie(
                "sessionId",
                userId, 
                httponly=True, 
                secure=False, 
                samesite="None", 
                max_age=60*60*24     # 1 day expiration
            )
            return response
        else:
            return jsonify({"success": False, "message": "Napačno geslo"})
    else:
        uporabnik = getUserUsername(identifier)
        if not uporabnik:
            return jsonify({"success": False, "message": "račun ne obstaja"})
        userId = uporabnik["userId"]
        if check_password_hash(uporabnik["hashPass"],password):
            response = make_response(jsonify({"success":True, "message":"Login uspešen"}))
            response.set_cookie(
                "sessionId",
                userId, 
                httponly=True, 
                secure=False, 
                samesite="None", 
                max_age=60*60*24     # 1 day expiration
            )
            return response
        else:
            return jsonify({"success": False, "message": "Napačno geslo"})
