from fastapi import APIRouter, Depends, HTTPException, Response, Request, File, UploadFile, Form
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta
from typing import Union

from ..database.creators.models import Option, Poll, Question, QuestionResult, Results, Reward, UserRewards, UserPoints
from ..database.servicesDb.databaseServ import getClaimeRewardId, savePoll, getCityId, getAllPolls, saveResults, getUserPoints, getPollId,getResultsId, getQuestionId,markCompletedPoll, moveToArchive, saveReward, getAllRewardsCity, getClaimedRewards, getRewardId, claimReward,updatePoints, moveRewardToArchive

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

class RewardRequest(BaseModel):
    rewardTitle: str
    rewardDescription: str
    pointsRequired: int
    expirationDate: datetime


class EditRewardRequest(BaseModel):
    id: str
    rewardTitle: str
    rewardDescription: str
    pointsRequired: int
    expirationDate: datetime

class RewardAllResponse(BaseModel):
    avaliableRewards: list[Reward]
    claimedRewards: list[Reward]

class DeleteClaimRewardRequest(BaseModel):
    id: str


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

@router.post("/addReward", response_model=PollResponse)
async def addRewardRoute(rewardRequest: RewardRequest, request: Request):
    adminId = request.cookies.get("sessionId")
    if not adminId:
        raise HTTPException(status_code=401, detail="Unauthorized, no admin ID")
    userCity = await getCityId(adminId)
    rewardID = uuid4()
    novReward = Reward(
        id=str(rewardID),
        creatorId=adminId,
        city=userCity,
        rewardTitle=rewardRequest.rewardTitle,
        rewardDescription=rewardRequest.rewardDescription,
        pointsRequired=rewardRequest.pointsRequired,
        creationDate=datetime.utcnow(),
        expirationDate=rewardRequest.expirationDate
    )
    await saveReward(novReward)
    return {"statusCode": 200, "message": "Reward added successfully"}

@router.get("/getAllAvailableRewards", response_model=RewardAllResponse)
async def getAllRewardsRoute(request: Request):
    avaliableRewards = []
    claimedRewards = []
    userId = request.cookies.get("sessionId")

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
    return {"avaliableRewards": avaliableRewards, "claimedRewards": claimedRewards}

@router.get("/getAllRewardsAdmin", response_model=list[Reward])
async def getAllRewardsAdminRoute(request: Request):
    adminId = request.cookies.get("sessionId") # spremen da realno čekira če je admin
    if not adminId:
        raise HTTPException(status_code=401, detail="Unauthorized, no admin ID")
    city = await getCityId(adminId)
    rewards = await getAllRewardsCity(city)
    return rewards

@router.post("/deleteReward", response_model=PollResponse)
async def deleteRewardRoute(deleteRewardRequest: DeleteClaimRewardRequest, request: Request):
    adminId = request.cookies.get("sessionId") # spremen da realno čekira če je admin
    if not adminId:
        raise HTTPException(status_code=401, detail="Unauthorized, no admin ID")
    reward = await getRewardId(deleteRewardRequest.id)
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    await moveRewardToArchive(reward)
    return {"statusCode": 200, "message": "Reward deleted successfully"}


#if admin pol all rewards, unclaimable samo na managmentu. to lahko preverjaš če je session id v admin idju

#če ni pogleda če si že claimou, in vrne list ( v obeh primerih list rewardov)

#popa claimRewardRoute pa admin da edita reward (npr. če je potekel, če je spremenil točke al pa kaj drugega)
#se delete rewardRoute
# 3 razlicna post routa

@router.post("/claimReward", response_model=PollResponse)
async def claimRewardRoute(claimRewardRequest: DeleteClaimRewardRequest, request:Request):
    userId = request.cookies.get("sessionId")
    if not userId:
        raise HTTPException(status_code=401, detail="Unauthorized, no user ID")
    reward = await getRewardId(claimRewardRequest.id)
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    userPoints = await getUserPoints(userId)
    if userPoints.points < reward.pointsRequired:
        raise HTTPException(status_code=400, detail="Not enough points to claim this reward")
    
    await updatePoints(userId, reward.pointsRequired, "-")
    await claimReward(userId, claimRewardRequest.id)
    return {"statusCode": 200, "message": "Reward claimed successfully"}




@router.post("/editReward", response_model=PollResponse)
async def editRewardRoute(rewardRequest: EditRewardRequest, request: Request):
    adminId = request.cookies.get("sessionId")
    if not adminId: # spremen da realno čekira če je admin
        raise HTTPException(status_code=401, detail="Unauthorized, no admin ID")
    reward = await getRewardId(rewardRequest.id)
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    reward.rewardTitle = rewardRequest.rewardTitle
    reward.rewardDescription = rewardRequest.rewardDescription
    reward.pointsRequired = rewardRequest.pointsRequired
    if rewardRequest.expirationDate < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Cannot set expiration date to a past date")
    reward.expirationDate = rewardRequest.expirationDate
    await saveReward(reward)
    return {"statusCode": 200, "message": "Reward edited successfully"}
#edit, delete, pa claim
# za vsak reward vrne kok jih je claimal
