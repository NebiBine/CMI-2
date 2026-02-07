from odmantic import AIOEngine
from pydantic import BaseModel
from ..creators.models import Cities, Announcments, Uporabnik, Profile, Admins, Reset, Poll, Results, UserPoints, PollArchive, Reward, UserRewards, RewardArchive, ResultsArchive, Current, DayForecast, Forecast, Alert, CityWeather, WeatherData
from datetime import datetime
from typing import Optional
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

async def getAllArchivedPolls(city: str):
    return await engine.find(PollArchive, PollArchive.city == city)

async def saveResults(results: Results):
    await engine.save(results)

async def markCompletedPoll(userId: str, pollId: str, points: int):
    userPoints = await engine.find_one(UserPoints, UserPoints.userId == userId)
    if not userPoints:
        userPoints = UserPoints(userId=userId, points=points, completedPolls=[])
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

async def getArchivedPollId(pollId: str):
    return await engine.find_one(PollArchive, PollArchive.id == pollId)

async def getResultsId(pollId: str):
    return await engine.find_one(Results, Results.pollId == pollId)

async def getArchivedResultsId(pollId: str):
    return await engine.find_one(ResultsArchive, ResultsArchive.pollId == pollId)

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
        questions = poll.questions,
        deletedAt=datetime.utcnow()
    )

    await engine.save(novArchive)
    await engine.delete(poll)

    results = await getResultsId(poll.id)

    novResults = ResultsArchive(
        id = results.id,
        pollId = results.pollId,
        answers = results.answers
        )
    await engine.save(novResults)
    await engine.delete(results)
    
    

async def saveReward(reward):
    await engine.save(reward)

async def getAllRewardsCity(city: str):
    return await engine.find(Reward, Reward.city == city)

async def getAllRewards(city: str):
    return await engine.find(Reward, Reward.city == city)

async def getClaimedRewards(userId: str):
    return await engine.find(UserRewards, UserRewards.userId == userId)

async def getClaimeRewardId(rewardId:str):
    return await engine.find_one(UserRewards, UserRewards.rewardId == rewardId)


async def getRewardId(rewardId: str):
    return await engine.find_one(Reward, Reward.id == rewardId)

async def claimReward(userId: str, rewardId: str):
    userReward = UserRewards(
        userId=userId,
        rewardId=rewardId,
        claimedAt=datetime.utcnow()
    )
    await engine.save(userReward)

async def updatePoints(userId: str, points: int, operation: str):
    userPoints = await engine.find_one(UserPoints, UserPoints.userId == userId)
    if not userPoints:
        userPoints = UserPoints(userId=userId, points=0, completedPolls=[])
    if operation == "+":
        userPoints.points += points
    elif operation == "-":
        userPoints.points -= points
    await engine.save(userPoints)

async def moveRewardToArchive(reward: Reward):
    novArchive = RewardArchive(
        id = reward.id,
        creatorId = reward.creatorId,
        city=reward.city,
        rewardTitle = reward.rewardTitle,
        rewardDescription = reward.rewardDescription,
        pointsRequired = reward.pointsRequired,
        creationDate = reward.creationDate,
        expirationDate = reward.expirationDate,
        deletedAt=datetime.utcnow()
    )

    await engine.save(novArchive)
    await engine.delete(reward)

async def saveAnnouncement(announcement: Announcments):
    await engine.save(announcement)

async def getAnnouncement(city: str):
    return await engine.find(Announcments, Announcments.city == city)

async def deleteAnnouncement(announcement: Announcments):
    await engine.delete(announcement)

#weather
async def saveWeatherData(weatherData: WeatherData):
    existingData = await engine.find_one(WeatherData)
    if existingData:
        existingData.weatherByCity = weatherData.weatherByCity
        existingData.lastUpdated = datetime.utcnow()
        await engine.save(existingData)
    else:
        await engine.save(weatherData)
    return

"""async def getCities():
    profiles = await engine.find(Profile)
    cities = []
    for profile in profiles:
        if(profile.city not in cities):
            cities.append(profile.city)
        else:
            continue
    return list(cities)"""


async def getWeatherData(city: str):
    weatherData = await engine.find_one(WeatherData)
    WeatherDataCity = weatherData.weatherByCity.get(city) if weatherData else None
    if weatherData:
        return weatherData.weatherByCity[city]
    return ""

#cities
async def saveCity(city: Cities):
    existingCity = await engine.find_one(Cities, Cities.city == city.city)
    if not existingCity:
        await engine.save(city)

async def getAllCities():
    cities = await engine.find(Cities)
    return [city.city for city in cities]

async def deleteCity(city: Cities):
    await engine.delete(city)