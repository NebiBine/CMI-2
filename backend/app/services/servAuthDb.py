from tinydb import TinyDB, Query
from datetime import datetime

database = TinyDB("databases/authDatabase.json")
uporabniki = database.table('uporabniki') #userId, name, password, email
reset = database.table('reset')# id, email, expire
admins = database.table('admins') # id


User = Query()

def getAll(table):
    return database.table(table)

def getUserUsername(username):
    return uporabniki.get(User.username == username)

def getUserMail(mail):
    print(mail)
    return uporabniki.get(User.email == mail)

def register(userId, username, hashPass, email):
    uporabniki.insert({
        "userId":userId,
        "username":username,
        "hashPass":hashPass,
        "email":email
    })
    return

def newPassword(hashPass, mail):
    uporabniki.update({"hashPass":hashPass}, User.email == mail)
    print("servDb-dela")
    return

def requestReset(resetId,email,expire):
    reset.insert({"resetId":resetId, "email":email, "expire": expire.isoformat()})


def getResetId(resetId):
    Id = Query()
    return reset.get(Id.resetId == resetId)

def delResetId(resetId):
    Id = Query()
    reset.remove(Id.resetId == resetId)

def addAdminDb(userId):
    admins.insert({"userId":userId})

def checkAdmin(userId):
    #admin = admins.get(User.userId == userId)
    if admins.get(User.userId == userId) != None:
        return True
    else:
        return False

