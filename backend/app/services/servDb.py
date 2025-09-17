from tinydb import TinyDB, Query

database = TinyDB("database.json")
uporabniki = database.table('uporabniki') #userId, name, password, email

User = Query()

def getAll(table):
    return database.table(table)

def getUserUsername(username):
    return uporabniki.get(User.username == username)

def getUserMail(mail):
    return uporabniki.get(User.mail == mail)

def register(userId, username, hashPass, email):
    uporabniki.insert({
        "userId":userId,
        "username":username,
        "hashPass":hashPass,
        "email":email
    })
    return