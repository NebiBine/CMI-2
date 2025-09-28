from flask import Blueprint, request, jsonify
from app.services.servProfileDb import getProfileInfo
dataBp = Blueprint("data", __name__, url_prefix="/data")

@dataBp.route("/getProfile", methods=["GET"])
def getProfile():
    userId = request.cookies.get("sessionId")
    print(userId)
    return getProfileInfo(userId)
