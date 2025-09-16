from flask import Blueprint, request, jsonify
from app.services.servUser import registerUser

authBp = Blueprint("auth", __name__, url_prefix="/auth")



@authBp.route("/register", methods=["POST"])
def register():
    #frontend posle ime, geslo
    data = request.json
    registerUser(data["username"], data["password"], data["email"])
    return jsonify({"msg": "Registered"}), 200

