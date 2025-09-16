from tinydb import TinyDB, Query

database = TinyDB("database.json")
uporabniki = database.table('uporabniki') #userId, name, password, email

def getAll(table):
    return database.table(table)

def register(userId, username, hashPass, email):
    uporabniki.insert({
        "userId":userId,
        "username":username,
        "hashPass":hashPass,
        "email":email
    })
    return