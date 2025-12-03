from tinydb import TinyDB, Query
from datetime import datetime

database = TinyDB("databases/profileDatabase.json",encoding="utf-8")
profile = database.table('profile') #userId, name, password, email

User = Query()

def newProfile(userId, name, username, birth, phone, street, city, country, zip, path):
    try:
        profile.insert({
            "userId":userId,
            "fullName": name, 
            "username": username,
            "birth": birth,
            "phone":phone,
            "street": street,
            "city": city,
            "country": country,
            "zip":zip,
            "pfpPath":path
        })
    except Exception as e:
        print(e)
    return

def getProfileInfo(userId):
    try:
        data = profile.get(User.userId == userId)
        print(data)
        return data
    except:
        return "vrjetn profil ne obstaja alpa nis loginan"
    
def updateUser(userId, name, username, birth, phone, street, city, country, zip):

    try:
        profile.update({
            "fullName": name, 
            "username": username,
            "birth": birth,
            "phone":phone,
            "street": street,
            "city": city,
            "country": country,
            "zip":zip,
        },
        User.userId == userId)
        return getProfileInfo(userId)
    except:
        return None
    
def getCity(userId):
    profil = profile.get(User.userId == userId)
    city = profil["city"]
    return city