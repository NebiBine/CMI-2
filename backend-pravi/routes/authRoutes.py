from fastapi import APIRouter, HTTPException, Response, Request, Form
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta
import re
import bcrypt

from ..services.email import sendEmail
from ..database.creators.models import Uporabnik, Reset
from ..database.servicesDb.databaseServ import getAllUsersDb, getUserId, getUserEmail, getUserUsername, saveUser, saveReset, getResetToken, deleteResetToken, addAdmin, getAdminId

router = APIRouter()

#modeli za requeste
class NewUser(BaseModel):
    username: str
    email: str
    password: str

class Tuser(BaseModel):
    identifier: str  # can be username or email
    password: str
    remember: bool

#model za response
class UserResponse(BaseModel):
    statusCode: int
    message: str

class UporabnikResponse(BaseModel):
    id: str
    email: str
    username: str
    password: str

class forgotPasswordRequest(BaseModel):
    email: str

class resetPasswordRequest(BaseModel):
    token: str
    newPassword: str

@router.post("/register", response_model=UserResponse)
async def register(user: NewUser, response: Response):
    print("dsjdsdsdsdsdsd")
    existingUser = await getUserUsername(user.username)
    if existingUser:
        raise HTTPException(status_code=400, detail="Username already registered")
    hash = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    hashPass = hash.decode("utf-8")
    userId = str(uuid4())
    novUser = Uporabnik(id=userId,username=user.username,email=user.email,password=hashPass)
    await saveUser(novUser)
    print("lala")
    response.set_cookie(
        key="sessionId", 
        value=userId,
        path="/",
        httponly=False, #to spreminjej za production
        secure=False, #to tud
        samesite="lax",
        max_age=3600*24  # 1 day
    )

    return {"statusCode": 200, "message": "User registered successfully"}

@router.post("/login",response_model=UserResponse)
async def login(user: Tuser, response: Response):
    EMAILPATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(EMAILPATTERN, user.identifier):
        existingUser = await getUserEmail(user.identifier)
        if not existingUser:
            raise HTTPException(status_code=400, detail="Invalid email")
        else:
            if not bcrypt.checkpw(user.password.encode('utf-8'), existingUser.password.encode('utf-8')):
                raise HTTPException(status_code=400, detail="Invalid password")
            userId = existingUser.id
            if user.remember:
                maxAge = 3600 * 24 * 7 * 30  # 1 month
            else:
                maxAge = 3600 * 24  # 1 day
            response.set_cookie(
                key="sessionId", 
                value=userId,
                path="/",
                httponly=False, #to spreminjej za production
                secure=False,
                samesite="lax",
                max_age=maxAge
            )
            return {"statusCode": 200, "message": "Login successful"}
    else:
        existingUser = await getUserUsername(user.identifier)
        if not existingUser:
            raise HTTPException(status_code=400, detail="Invalid username")
        else:
            if not bcrypt.checkpw(user.password.encode('utf-8'), existingUser.password.encode('utf-8')):
                raise HTTPException(status_code=400, detail="Invalid password")
            userId = existingUser.id
            if user.remember:
                maxAge = 3600 * 24 * 7 * 30  # 1 month
            else:
                maxAge = 3600 * 24  # 1 day
            response.set_cookie(
                key="sessionId", 
                value=userId,
                path="/",
                httponly=False, #to spreminjej za production
                secure=False,
                samesite="lax",
                max_age=maxAge
            )
            return {"statusCode": 200, "message": "Login successful"}
    
@router.post("/logout",response_model=UserResponse)
async def logout(response: Response):
    pass

@router.post("/addAdmin",response_model=UserResponse)
async def addAdmin():
    pass

@router.get("/check")
async def check(request: Request):
    userId = request.cookies.get("sessionId")
    if userId:
        return {"loggedIn": True}
    else:
        return {"loggedIn": False}
    
@router.get("/checkAdmin")
async def checkAdmin(request: Request):
    userId = request.cookies.get("sessionId")
    if userId:
        return {"admin": True}
    #NE DOKONČANO, do productiona dodt še preverjanje če je user admin ds dsds
    return {"admin": False}

@router.post("/forgotPassword")
async def forgotPassword(email: forgotPasswordRequest): 
    user = await getUserEmail(email.email)
    if not user:
        raise HTTPException(status_code=400, detail="Email not found")
    userId = user.id
    token = str(uuid4())
    expiresAt = datetime.utcnow() + timedelta(hours=1)
    resetEntry = Reset(userId=userId, token=token, expiry=expiresAt)
    await saveReset(resetEntry)

    resetLink = f"http://localhost:5173/auth/PasswordReset/{token}"

    sendEmail(email.email, resetLink)
    
    return {"statusCode": 200, "message": "Password reset link has been sent to your email"}

@router.post("/resetPassword")
async def resetPassword(resetData: resetPasswordRequest):
    reset = await getResetToken(resetData.token)
    if not reset:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    if reset.expiry < datetime.utcnow():
        await deleteResetToken(reset)
        raise HTTPException(status_code=400, detail="Token has expired")
    user = await getUserId(reset.userId)
    
    hashPass = bcrypt.hashpw(resetData.newPassword.encode('utf-8'), bcrypt.gensalt())
    user.password = hashPass.decode('utf-8')
    await saveUser(user)
    await deleteResetToken(reset)
    
    return {"statusCode": 200, "message": "Password has been reset successfully"}

@router.get("/testEndpoint", response_model=UporabnikResponse)
async def testEndpoint():
    return await getUserEmail("bine")

@router.get("/getProfile")
async def getProfile(request: Request):
    userId = request.cookies.get("sessionId")
    if not userId:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = await getUserId(userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username}

@router.get("/getAllUsers")
async def getAllUsers():
    return await getAllUsersDb()