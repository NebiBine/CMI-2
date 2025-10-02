from flask import Blueprint, request, jsonify
from app.services.servProfileDb import getProfileInfo
from app.services.servAuthDb import getAll
dataBp = Blueprint("data", __name__, url_prefix="/data")

@dataBp.route("/getProfile", methods=["GET"])
def getProfile():
    userId = request.cookies.get("sessionId")
    print(userId)
    return getProfileInfo(userId)

@dataBp.route("/getAllUsers", methods=["GET"])
def getAllUsers():
    print(getAll("uporabniki"))
    return getAll("uporabniki")