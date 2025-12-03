from .servProfileDb import getCity
from .servPollDb import addPollDb
from datetime import datetime, timedelta
import uuid
from flask import jsonify

def servAddPoll(duration, worth, questionsRaw, admin, name):
    city = getCity(admin)
    dateAdded = datetime.now()
    expiryDate = dateAdded + timedelta(days = duration)
    questions = {}
    for key, q in questionsRaw.items():
        tempId = str(uuid.uuid4())
        if q["type"] in ["input", "yesno"]:  
            questions[f"q_{tempId}"] = {
                "qId" : tempId,
                "upr" : q["uprasanje"],
                "type" : q["type"]
            }
        elif q["type"] in ["check", "radio"]:
            options = {}
            for key,o in q["options"].items():
                tempIdOptions = str(uuid.uuid4())
                options[f"o_{tempIdOptions}"] = {
                    "oId":tempIdOptions,
                    "o":o
                }
            questions[f"q_{tempId}"] = {
                "qId": tempId,
                "upr": q["uprasanje"],
                "type":q["type"],
                "options":options
            }
    pollId = str(uuid.uuid4())
    if addPollDb(duration, worth, questions, admin, city, dateAdded, expiryDate, pollId, name) == True:
        return jsonify({"success":True, "message": "poll added successfuly"}),200
    else:
        return jsonify({"success":False, "message": "error with adding polls"}),500
    

