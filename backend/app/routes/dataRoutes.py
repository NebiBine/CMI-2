from flask import Blueprint, request, jsonify, Flask
import flask
from app.services.servProfileDb import getProfileInfo, updateUser
from app.services.servAuthDb import getAllTables, checkAdmin
from app.services.servUser import addAdmin
dataBp = Blueprint("data", __name__, url_prefix="/data")

@dataBp.route("/getProfile", methods=["POST", "GET"])
def getProfile():
    if flask.request.method == "POST":
        userId = request.json["userId"]
        print(userId +"------------------------------------------------------------------")
        data = getProfileInfo(userId)
        isAdmin = checkAdmin(userId)
        print(isAdmin)
        data["isAdmin"] = isAdmin
        print(data)
        return data
    else:
        #manage profile isto samo get ker bo vleku iz cookija id
        userId = request.cookies.get("sessionId")
        return getProfileInfo(userId)

@dataBp.route("/getAllUsers", methods=["GET"])
def getAllUsers():
    return getAllTables()

@dataBp.route("/updateUser", methods=["POST"])
def updateUserR():
    data=request.json
    print(data)
    if data["isAdmin"] == True:
        if addAdmin(data["userId"]) == True:
            uud = updateUser(data["userId"], data["fullName"],data["username"],data["birth"],data["phone"],data["street"],data["city"],data["country"],data["zip"],)
            uud["isAdmin":True]
            return uud
        else:
            uud = updateUser(data["userId"], data["fullName"],data["username"],data["birth"],data["phone"],data["street"],data["city"],data["country"],data["zip"],)
            uud["isAdmin":False]
            return uud
        

""""
updateUser prcakuje:
    data = {
    "userId":123,
    "Fullname":fullName,
    "username":username,
    "birth":birth,
    "phone":phone,
    "street":street,
    "city":city,
    "country":country,
    "zip":zip,
    }
"""
"""
{
  "profile": {
    "1": {
      "userId": "3cb33496-96dc-493d-8842-78ff8ff0b96c",
      "fullName": "Bine Tavčar",
      "username": "Nebi",
      "birth": "1. 5. 2007",
      "phone": "064297766",
      "street": "ŠKOFJELOŠKA CESTA 5",
      "city": "Ljubljana",
      "country": "Slovenija",
      "zip": "1217",
      "pfpPath": "databases\\pfps\\pfp3cb33496-96dc-493d-8842-78ff8ff0b96c.png"
    },
    "2": {
      "userId": "89f644c0-336f-4cc5-92d7-02dc83df3f2a",
      "fullName": "Nace Rozman",
      "username": "nace",
      "birth": "21. 3. 2007",
      "phone": "051369536",
      "street": "Mestni trg 37",
      "city": "Škofja Loka",
      "country": "Slovenia",
      "zip": "4220",
      "pfpPath": "databases\\pfps\\pfp89f644c0-336f-4cc5-92d7-02dc83df3f2a.png"
    }
  }
}

"""