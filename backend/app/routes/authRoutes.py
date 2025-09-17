from flask import Blueprint, request, jsonify
from app.services.servUser import registerUser, loginUser

authBp = Blueprint("auth", __name__, url_prefix="/auth")



@authBp.route("/register", methods=["POST"])
def register():
    #frontend posle ime, geslo
    data = request.json
    registerUser(data["username"], data["password"], data["email"])
    return jsonify({"msg": "Registered"}), 200

@authBp.route("/login", methods=["POST"])
def login():
    data = request.json
    loginUser(data["identifier"], data["password"])
    #cooks
    #return
