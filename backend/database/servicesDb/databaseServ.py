from odmantic import AIOEngine
from ..creators.models import Uporabnik, Profile, Admins, Reset, Poll, Results, UserPoints, PollArchive

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
async def savePoll(poll: Poll):
    await engine.save(poll)

async def getAllPolls(city: str):
    return await engine.find(Poll, Poll.city == city)

async def saveResults(results: Results):
    await engine.save(results)

async def markCompletedPoll(userId: str, pollId: str, points: int):
    userPoints = await engine.find_one(UserPoints, UserPoints.userId == userId)
    if not userPoints:
        userPoints = UserPoints(userId=userId, points=0, completedPolls=[])
    if pollId not in userPoints.completedPolls:
        userPoints.points += points
        userPoints.completedPolls.append(pollId)
        await engine.save(userPoints)

async def getUserPoints(userId: str):
    userPoints = await engine.find_one(UserPoints, UserPoints.userId == userId)
    if not userPoints:
        userPoints = UserPoints(userId=userId, points=0, completedPolls=[])
        await engine.save(userPoints)
    return userPoints

async def getPollId(pollId: str):
    return await engine.find_one(Poll, Poll.id == pollId)

async def getResultsId(pollId: str):
    return await engine.find_one(Results, Results.pollId == pollId)

async def updatePollResults(pollId: str, answers: list):
    pass

async def getQuestionId(questionId: str, ResultsObj: Results):
    return ResultsObj.answers.get(questionId)

async def moveToArchive(poll: Poll):
    novArchive = PollArchive(
        id = poll.id,
        creatorId = poll.creatorId,
        city=poll.city,
        pollTitle = poll.pollTitle,
        pollDescription = poll.pollDescription,
        pollDuration = poll.pollDuration,
        expirationDate = poll.expirationDate,
        creationDate = poll.creationDate,
        points = poll.points,
        questions = poll.questions
    )

    await engine.save(novArchive)
    await engine.delete(poll)


    