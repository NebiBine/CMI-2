from fastapi import APIRouter, Depends, HTTPException, Response, Request, File, UploadFile, Form
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Union

from ..database.creators.models import Option, Poll, Question, QuestionResult, Results
from ..database.servicesDb.databaseServ import savePoll, getCityId, getAllPolls, saveResults, getUserPoints, getPollId,getResultsId, getQuestionId,markCompletedPoll, moveToArchive

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

class UserAnswer(BaseModel):
    questionId: str
    questionText: str
    questionType: str
    answer: Union[str, list[str]]

class PollSubmissionRequest(BaseModel):
    pollId: str
    pollQuestions: list[UserAnswer]

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
        if poll.expirationDate < datetime.utcnow():
            await moveToArchive(poll)
            continue
        if poll.id not in completedPolls:
            compPolls.append(poll)

    return compPolls


@router.post("/completePoll", response_model=PollResponse)
async def completePollRoute(pollreq: PollSubmissionRequest, request: Request):
    userId = request.cookies.get("sessionId")
    if not userId:
        raise HTTPException(status_code=401, detail="Unauthorized, no user ID")
    pollId = pollreq.pollId
    poll = await getPollId(pollId)
    results = await getResultsId(pollId)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    for userAnswer in pollreq.pollQuestions:
        questionResult: QuestionResult = await getQuestionId(userAnswer.questionId, results)
        if userAnswer.questionType == "yesno":
            #{questionId: '2326882a-41e1-4af4-b14e-21c6bcdca1b6', questionText: 'waf', answer: 'aa'}
            if userAnswer.answer == "Yes":
                questionResult.option1.result.append(userId)
            else:
                questionResult.option2.result.append(userId)

        elif userAnswer.questionType == "input":
            questionResult.option1.result.append(userAnswer.answer)

        elif userAnswer.questionType == "radioButtons":
            if userAnswer.answer == questionResult.option1.optionText:
                questionResult.option1.result.append(userId)
            elif userAnswer.answer == questionResult.option2.optionText:
                questionResult.option2.result.append(userId)
            elif userAnswer.answer == questionResult.option3.optionText:
                questionResult.option3.result.append(userId)
            elif userAnswer.answer == questionResult.option4.optionText:
                questionResult.option4.result.append(userId)
        elif userAnswer.questionType == "checkbox":
            for ans in userAnswer.answer:
                if ans == questionResult.option1.optionText:
                    questionResult.option1.result.append(userId)
                elif ans == questionResult.option2.optionText:
                    questionResult.option2.result.append(userId)
                elif ans == questionResult.option3.optionText:
                    questionResult.option3.result.append(userId)
                elif ans == questionResult.option4.optionText:
                    questionResult.option4.result.append(userId)

    await saveResults(results)
    await markCompletedPoll(userId, pollId, poll.points)
    return {"statusCode": 200, "message": "Poll completed successfully"}
        
@router.get("/getUserPoints", response_model=int)
async def getUserPointsRoute(request: Request):
    userId = request.cookies.get("sessionId")
    if not userId:
        raise HTTPException(status_code=401, detail="Unauthorized, no user ID")
    userPoints = await getUserPoints(userId)
    return userPoints.points