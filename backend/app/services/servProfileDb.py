from tinydb import TinyDB, Query
from datetime import datetime

database = TinyDB("databases/profileDatabase.json")
profile = database.table('profile') #userId, name, password, email

User = Query()

def newProfile(userId, name, username, birth, phone, street, city, country, zip):
    profile.insert({
        "userId":userId,
        "fullName": name, 
        "username": username,
        "birth": birth,
        "phone":phone,
        "street": street,
        "city": city,
        "country": country,
        "zip":zip
    })
    return