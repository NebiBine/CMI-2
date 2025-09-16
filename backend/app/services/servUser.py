from app.model.user import User
from .servDb import getAll, register
from tinydb import Query, TinyDB
import uuid

UserQuery = Query()

def registerUser(username, password, email):
    users = getAll("uporabniki")
    if users.search(UserQuery.username == username):
        return
    user =User(username=username, email=email)
    user.MakePassword(password)
    user.id = uuid.uuid4()
    register(user.id,user.username, user.passwordHash, user.email)
