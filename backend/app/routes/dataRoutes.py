from flask import Blueprint, request, jsonify, Flask
import flask
from app.services.servProfileDb import getProfileInfo, updateUser
from app.services.servAuthDb import getAllTables, checkAdmin
from app.services.servUser import addAdmin, removeAdmin
from app.services.servPoll import servAddPoll
dataBp = Blueprint("data", __name__, url_prefix="/data")

@dataBp.route("/getProfile", methods=["POST", "GET"])
def getProfile():
    if flask.request.method == "POST":
        userId = request.json["userId"]
        print(userId +"------------------------------------------------------------------")
        data = getProfileInfo(userId) #--> PRINTA profil
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
        updateUser(data["userId"], data["fullName"],data["username"],data["birth"],data["phone"],data["street"],data["city"],data["country"],data["zip"],)

      else:
        updateUser(data["userId"], data["fullName"],data["username"],data["birth"],data["phone"],data["street"],data["city"],data["country"],data["zip"],)
    else:
        removeAdmin(data["userId"])
        updateUser(data["userId"], data["fullName"],data["username"],data["birth"],data["phone"],data["street"],data["city"],data["country"],data["zip"],)
    return jsonify({"success":True, "message":"succesfully updates"}), 200
        

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

#------------POLLS-------------------------
@dataBp.route("/addPoll", methods=['POST'])
def addPoll():
  data=request.json
  duration = data["duration"] #days
  worth = data["worth"]
  questions = data["questions"]
  name = data["name"]
  userId = request.cookies.get("sessionId")
  return servAddPoll(duration, worth, questions, userId, name)
     

  """
    "pollId":{
      "pollId":12345678,
      "admin":"bine",
      "dateAdd":123232,
      "duration":2d,
      "expiry":"dateAdd + duration",
      "city":"Ljubljana",
      "vrednost":15,
      "questions":{
          "qId1":{
            "name":"uprasanje",
            "qId":123456789,
            "uprasanje":"ALI SI VESEL",
            "type":"checkBox"
          }"qId2":{
            "name":"uprasanje",
            "qId":1234567891,
            "uprasanje":"kaj delas",
            "type":"textbox"
            ]
          }
      }
    }
  """


  """
  data = request.data
  data -> 
  {"data":{
    "duration": 2,
    "vrednost":15,
    "questions":{
        "q1":{
            "name":"traffic light",
            "uprasanje": "ali ti je vsec traffic light",
            "type":"yesno"
        },
        "q2":{
            "name":"suggestios",
            "uprasanje": "kaj bi dodali v mesto",
            "type":"input"
        }
        
    }
}
 
}
 return database add poll

 v db serv se nardi ta db in result db:

 result -> 
{
   "results":{
      "pollId":{
         "q1Id":{
            "question":"vprasanje",
            "type":"yesno",
            "res":{
               "yes":323,
               "no":323
            }
         },
         "q2Id":{
            "question":"vprasanje",
            "type":"input",
            "res":{
               "inputs":[
                  "dsdsd",
                  "dsdd"
               ]
            }
         },
         "q3Id":{
            "question":"vprasanje",
            "type":"check",
            "res":{
               "o1":232,
               "o2":234,
               "o3":343,
               "o4":222
            }
         },
         "q4Id":{
            "question":"vprasanje",
            "type":"radio",
            "res":{
               "o1":232,
               "o2":234,
               "o3":343,
               "o4":222
            }
         }
      }
   }
}
  """
  pass

@dataBp.route("/removePoll", methods=['POST'])
def addPoll():
  pass

@dataBp.route("/getPolls", methods=['POST'])
def addPoll():
  pass

@dataBp.route("/votePoll", methods=['POST'])
def addPoll():
  pass

@dataBp.route("/viewPoll", methods=['POST'])
def addPoll():
  pass