from odmantic import AIOEngine
from ..creators.models import Uporabnik, Profile, Admins, Reset, Poll

engine = AIOEngine()

#auth
async def getUserId(user_id: str):
    return await engine.find_one(Uporabnik, Uporabnik.id == user_id)

async def getUserEmail(email: str):
    return await engine.find_one(Uporabnik, Uporabnik.email == email)

async def getUserUsername(username: str):
    return await engine.find_one(Uporabnik, Uporabnik.username == username)

async def saveUser(user: Uporabnik):
    await engine.save(user)

async def saveReset(reset: Reset):
    await engine.save(reset)

async def getResetToken(token: str):
    return await engine.find_one(Reset, Reset.token == token)

async def deleteResetToken(reset: Reset):
    await engine.delete(reset)

async def addAdmin(admin: Admins):
    await engine.save(admin)

async def deleteAdmin(admin: Admins):
    await engine.delete(admin)

async def getAdminId(admin_id: str):
    return await engine.find_one(Admins, Admins.id == admin_id)

async def getAllUsersDb():
    return await engine.find(Uporabnik)
#profile

async def createProfile(profile: Profile):
    await engine.save(profile)

async def getProfileId(profile_id: str):
    return await engine.find_one(Profile, Profile.id == profile_id)

async def getCityId(id: str):
    profile = await engine.find_one(Profile, Profile.id == id)
    return profile.city

#polls
async def savePoll(poll):
    await engine.save(poll)

async def getAllPolls(city):
    return await engine.find(Poll, Poll.city == city)