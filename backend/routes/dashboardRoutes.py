from fastapi import APIRouter, Depends, HTTPException, Response, Request, Form
from pydantic import BaseModel

from backend.services.auth import AuthContext, requireUser
from ..database.creators.models import Announcments
from ..database.servicesDb.databaseServ import getCityId, getAnnouncement, saveAnnouncement, deleteAnnouncement
from uuid import uuid4
from datetime import datetime, timedelta

router = APIRouter()

class AnnouncementResponse(BaseModel):
    statusCode: int
    message: str

class AnnouncementRequest(BaseModel):
    title: str
    content: str
    type : str

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
