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
        if not uporabnik:
            return jsonify({"succes": False, "message": "račun ne obstaja"})
        uporabnik = getUserMail(identifier)
        userId = uporabnik["userId"]
        if check_password_hash(uporabnik["hashPass"],password):
            response = make_response(jsonify({"succes":True, "message":"Login uspešen"}))
            response.set_cookie(
                "sessionId",
                userId, 
                httponly=True, 
                secure=False, 
                samesite="None", 
                max_age=60*60*24     # 1 day expiration
            )
        else:
            return jsonify({"succes": False, "message": "Napačno geslo"})
    else:
        if not uporabnik:
            return jsonify({"succes": False, "message": "račun ne obstaja"})
        uporabnik = getUserUsername(identifier)
        userId = uporabnik["userId"]
        if check_password_hash(uporabnik["hashPass"],password):
            response = make_response(jsonify({"succes":True, "message":"Login uspešen"}))
            response.set_cookie(
                "sessionId",
                userId, 
                httponly=True, 
                secure=False, 
                samesite="None", 
                max_age=60*60*24     # 1 day expiration
            )
        else:
            return jsonify({"succes": False, "message": "Napačno geslo"})
