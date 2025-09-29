from flask import Blueprint, request, jsonify
from app.services.servUser import registerUser, loginUser 
from app.services.servReset import requestPassReset, resetPassword
from app.services.servProfile import servNewProfile

authBp = Blueprint("auth", __name__, url_prefix="/auth")

@authBp.route("/check", methods=["GET"])
def check_auth():
    userId = request.cookies.get("sessionId") 
    if userId:
        return jsonify({"loggedIn": True, "userId": userId}), 200
    else:
        return jsonify({"loggedIn": False}), 401

@authBp.route("/register", methods=["POST"])
def register():
    data = request.json
    return registerUser(data["username"], data["password"], data["email"])

@authBp.route("/login", methods=["POST"])
def login():
    data = request.json

    return loginUser(data["identifier"], data["password"],data["remember"])

@authBp.route("forgotPassword", methods=["POST"])
def forgotPass():
    data = request.json

    return requestPassReset(data["email"], data["token"], data["resetlink"])

@authBp.route("resetPassword/<token>", methods=["POST"])
def resetPass(token):
    data = request.json
    return resetPassword(token, data["newPassword"])

@authBp.route("newProfile", methods=["POST"])
def newProfile():
    userId = request.cookies.get("sessionId")
    return servNewProfile(userId, request.form.get("fullname"),request.form.get("username"),request.form.get("dateOfBirth"),request.form.get("phoneNumber"),request.form.get("street"),request.form.get("city"),request.form.get("country"),request.form.get("zip"),request.files.get("profilePicture"))


