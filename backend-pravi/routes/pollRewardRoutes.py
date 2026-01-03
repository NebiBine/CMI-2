from fastapi import APIRouter, Depends, HTTPException, Response, Request, File, UploadFile, Form
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta

from ..database.creators.models import Poll
from ..database.servicesDb.databaseServ import savePoll, getCityId, getAllPolls

router = APIRouter()

class PollResponse(BaseModel):
    statusCode: int
    message: str

class Question(BaseModel):
    text: str
    type: str
    options: list[str]

class PollRequest(BaseModel):
    pollTitle: str
    pollDuration: int  # in days
    points: int
    questions: list[Question]


@router.post("/addPoll", response_model=PollResponse)
async def addPollRoute(pollR: PollRequest, request: Request):
    adminId = request.cookies.get("sessionId")
    if not adminId:
        raise HTTPException(status_code=401, detail="Unauthorized, no admin ID")
    userCity = await getCityId(adminId)
    pollId = uuid4()
    expirationDate = datetime.utcnow() + timedelta(days=pollR.pollDuration)
    creationDate = datetime.utcnow()
    novPoll = Poll(id=str(pollId), creatorId=adminId, city=userCity, pollTitle=pollR.pollTitle, pollDuration=pollR.pollDuration, expirationDate=expirationDate, creationDate=creationDate, points=pollR.points, questions=pollR.questions)
    await savePoll(novPoll)
    return {"statusCode": 200, "message": "Poll added successfully"}

@router.get("/getPolls", response_model=list[Poll])
async def getPollsRoute(request: Request):
    userId = request.cookies.get("sessionId")
    if not userId:
        raise HTTPException(status_code=401, detail="Unauthorized, no user ID")
    city = await getCityId(userId)
    polls = await getAllPolls(city)
    return polls