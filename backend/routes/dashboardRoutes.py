from fastapi import APIRouter, Depends, HTTPException, Response, Request, Form
from pydantic import BaseModel

from backend.services.auth import AuthContext, requireUser
from ..database.creators.models import Announcments
from ..database.servicesDb.databaseServ import getAllPolls, getAllRewardsCity, getCityId, getAnnouncement, getClaimedRewards, getUserPoints, moveRewardToArchive, moveToArchive, saveAnnouncement, deleteAnnouncement
from uuid import uuid4
from datetime import datetime, timedelta

router = APIRouter()

# kok pollov na dash, kok kok rewardou na dash

class AnnouncementResponse(BaseModel):
    statusCode: int
    message: str

class AnnouncementRequest(BaseModel):
    title: str
    content: str
    type : str

class DashboardStatsResponse(BaseModel):
    polls: int
    rewards: int
    getClaimedRewards: int
    userPoints: int

@router.get("/getAnnouncement",response_model=list[Announcments])
async def getAnnouncementRoute(auth: AuthContext = Depends(requireUser)):
    userId = auth.userId
    city = await getCityId(userId)
    announcement = await getAnnouncement(city)
    if not announcement:
        return []
    elif announcement[0].expirationDate < datetime.utcnow():
        await deleteAnnouncement(announcement[0])
        return []
    return announcement

@router.get("/getStats",response_model=DashboardStatsResponse)
async def getStatsRoute(auth: AuthContext = Depends(requireUser)):
    userId = auth.userId
    city = await getCityId(userId)
    
    #polls
    polls = await getAllPolls(city)

    userPoints = await getUserPoints(userId)
    completedPolls = userPoints.completedPolls # to je list z narjenimi
    compPolls = []

    for poll in polls:
        if poll.expirationDate < datetime.utcnow():
            await moveToArchive(poll)
            continue
        if poll.id not in completedPolls:
            compPolls.append(poll)

    #rewards
    avaliableRewards = []
    claimedRewards = []
    userId = auth.userId

    if not userId:
        raise HTTPException(status_code=401, detail="Unauthorized, no user ID")
    claimedR = await getClaimedRewards(userId)
    claimedRewardIds = [claim.rewardId for claim in claimedR]
        
    city = await getCityId(userId)
    rewards = await getAllRewardsCity(city)

    for reward in rewards: # extra check za potekle rewarde
        if reward.expirationDate < datetime.utcnow():
            await moveRewardToArchive(reward)
            continue
        else:
            if reward.id not in claimedRewardIds:
                avaliableRewards.append(reward)
            else:
                claimedRewards.append(reward)

    return {"polls": len(compPolls), "rewards": len(avaliableRewards), "getClaimedRewards": len(claimedRewards), "userPoints": userPoints.points}


@router.post('/createAnnouncement',response_model=AnnouncementResponse)
async def createAnnouncementRoute(auth: AuthContext = Depends(requireUser), announcement: AnnouncementRequest = None):
    adminId = auth.userId
    city = await getCityId(adminId)
    ann = await getAnnouncement(city)
    if len(ann) > 0:
        return {"statusCode": 400, "message": "Announcement for this city already exists"}
    newAnnouncement = Announcments(
        id = str(uuid4()),
        city = city,
        title=announcement.title,
        content=announcement.content,
        expirationDate=datetime.utcnow() + timedelta(days=7),
        type = announcement.type
    )
    await saveAnnouncement(newAnnouncement)
    return {"statusCode": 200, "message": "Announcement created successfully"}

#TODO DELETE ANNOUNCEMENT IF NEEDED

"""
class Announcments(Model):
    id: str = Field(primary_field=True, default_factory=lambda: str(uuid4()))
    city: str
    title: str
    content: str
    expirationDate: datetime
"""
