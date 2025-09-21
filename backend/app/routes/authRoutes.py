from flask import Blueprint, request, jsonify
from app.services.servUser import registerUser, loginUser 
from app.services.servReset import requestPassReset, resetPassword

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

@authBp.route("forgotPassword", methods=["POST"])
def forgotPass():
    data = request.json
    print(data)
    requestPassReset(data["email"], data["token"], data["resetlink"])
    return jsonify({"message": "Email sent succesfully", "success":True})

@authBp.route("resetPassword/<token>", methods=["POST"])
def resetPass(token):
    data = request.json
    resetPassword(token, data["newPassword"])
    print(data)
    return jsonify({"success":True, "message": "dela"})

