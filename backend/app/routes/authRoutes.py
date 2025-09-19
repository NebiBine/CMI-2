from flask import Blueprint, request
from app.services.servUser import registerUser, loginUser

authBp = Blueprint("auth", __name__, url_prefix="/auth")

@authBp.route("/register", methods=["POST"])
def register():
    data = request.json
    return registerUser(data["username"], data["password"], data["email"])

@authBp.route("/login", methods=["POST"])
def login():
    data = request.json
    print(data)
    return loginUser(data["identifier"], data["password"])

    
