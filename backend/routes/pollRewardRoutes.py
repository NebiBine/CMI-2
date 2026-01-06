from fastapi import APIRouter, Depends, HTTPException, Response, Request, File, UploadFile, Form
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta

from ..database.creators.models import Option, Poll, Question, QuestionResult, Results
from ..database.servicesDb.databaseServ import savePoll, getCityId, getAllPolls, saveResults, getUserPoints

router = APIRouter()

class PollResponse(BaseModel):
    statusCode: int
    message: str

class PollRequest(BaseModel):
    pollTitle: str
    pollDuration: int  # in days
    pollDescription: str
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
    for q in pollR.questions:
        q.id = str(uuid4())
    novPoll = Poll(id=str(pollId), creatorId=adminId, city=userCity, pollTitle=pollR.pollTitle, pollDescription=pollR.pollDescription, pollDuration=pollR.pollDuration, expirationDate=expirationDate, creationDate=creationDate, points=pollR.points, questions=pollR.questions)
    await savePoll(novPoll)
    answers = {}
    for q in pollR.questions:
        answers[q.id] = QuestionResult(
            questionId=q.id,
            questionType=q.type,
            questionText=q.text,
            option1=Option(optionText=q.options[0], result=[]),
            option2=Option(optionText=q.options[1], result=[]),
            option3=Option(optionText=q.options[2], result=[]),
            option4=Option(optionText=q.options[3], result=[])
        )
    
    novResults = Results(pollId=str(pollId), answers=answers)
    await saveResults(novResults)
    return {"statusCode": 200, "message": "Poll added successfully"}

@router.get("/getPolls", response_model=list[Poll])
async def getPollsRoute(request: Request):
    userId = request.cookies.get("sessionId")
    if not userId:
        raise HTTPException(status_code=401, detail="Unauthorized, no user ID")
    city = await getCityId(userId)
    polls = await getAllPolls(city)

    userPoints = await getUserPoints(userId)
    completedPolls = userPoints.completedPolls # to je list z narjenimi

    compPolls = []

    for poll in polls:
        if poll.id in completedPolls:
            compPolls.append(poll.id)

    return compPolls

@router.get("/completePoll")
async def completePollRoute(pollId: str, request: Request):
    pass
    #  markCompletedPoll iz serva
    # shran odgovore v results