from fastapi import APIRouter, HTTPException, Response, Request, Form
from pydantic import BaseModel
from ..database.creators.models import Announcments
from ..database.servicesDb.databaseServ import getCityId, getAnnouncment, saveAnnouncment, deleteAnnouncment
from uuid import uuid4
from datetime import datetime, timedelta

router = APIRouter()

class AnnouncmentResponse(BaseModel):
    statusCode: int
    message: str

class AnnouncmentRequest(BaseModel):
    title: str
    content: str

@router.get("/getAnnouncment",response_model=list[Announcments])
async def getAnnouncmentRoute(request : Request):
    userId = request.cookies.get("sessionId")
    if not userId:
        raise HTTPException(status_code=401, detail="Unauthorized, no user ID")
    city = await getCityId(userId)
    announcment = await getAnnouncment(city)
    if not announcment:
        return []
    elif announcment[0].expirationDate < datetime.utcnow():
        await deleteAnnouncment(announcment[0])
        return []
    return announcment


@router.post('/createAnnouncment',response_model=AnnouncmentResponse)
async def createAnnouncmentRoute(request:Request, announcment: AnnouncmentRequest):
    adminId = request.cookies.get("sessionId")
    if not adminId:
        raise HTTPException(status_code=401, detail="Unauthorized, no admin ID")
    city = await getCityId(adminId)
    novAnnouncment = Announcments(
        id = str(uuid4()),
        city = city,
        title=announcment.title,
        content=announcment.content,
        expirationDate=datetime.utcnow() + timedelta(days=7)
    )
    await saveAnnouncment(novAnnouncment)
    return {"statusCode": 200, "message": "Announcment created successfully"}



"""
class Announcments(Model):
    id: str = Field(primary_field=True, default_factory=lambda: str(uuid4()))
    city: str
    title: str
    content: str
    expirationDate: datetime
"""
