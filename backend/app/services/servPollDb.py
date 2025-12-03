from tinydb import TinyDB, Query


database = TinyDB("databases/pollsDatabase.json",encoding="utf-8")
polls = database.table('polls')
results = database.table('results')

User = Query()

def addPollDb(duration, worth, questions, admin, city, dateAdded, expiryDate, pollId, name):
    try:
        polls.insert({
            "pollid":pollId,
            "name":name,
            "admin":admin,
            "dateAdded":dateAdded,
            "duration":duration,
            "expiryDate": expiryDate,
            "city":city,
            "worth":worth,
            "questions":questions
        })
        makeResultsDb(questions, pollId, city, duration, admin)
        return True
    except:
        return False
    
def makeResultsDb(questions, pollId, city,duration,admin):
    try:
        questionsa = {}
        for qkey, q in questions.items():
            if q["type"] in ["check","radio"]:
                qId = q["qId"]
                optionsa = {}
                for okey, o in q["options"].items():
                    optionsa[f"_{o["oId"]}"] = {
                        "oId": o["oId"],
                        "votes":0
                    }
                questionsa[f"q_{qId}"] = {
                    "name" : q["name"],
                    "qId" : qId,
                    "upr" : q["upr"],
                    "type": q["type"],
                    "options": optionsa
                }

            elif q["type"] in ["yesno"]:
                qId = q["qId"]
                questionsa[f"q_{qId}"] = {
                    "name" : q["name"],
                    "qId" : qId,
                    "upr" : q["upr"],
                    "type": q["type"],
                    "options":{
                        "yes":0,
                        "no":0
                    }
                }

            elif q["type"] in ["input"]:
                qId = q["qId"]
                questionsa[f"q_{qId}"] = {
                    "name" : q["name"],
                    "qId" : qId,
                    "upr" : q["upr"],
                    "type": q["type"],
                    "options":{
                        "answers":[]
                    }
                }

        results.insert({
            "pollId":pollId,
            "city":city,
            "admin":admin,
            "duration":duration,
            "questions":questionsa
        })
    except:
        pass
