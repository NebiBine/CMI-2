from fastapi import APIRouter, Depends, HTTPException, Response, Request, Form
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta
import re
import bcrypt

from ..services.email import sendEmail
from ..database.creators.models import Session, Uporabnik, Reset
from ..database.servicesDb.databaseServ import saveCity, getAllUsersDb, getUserId, getUserEmail, getUserUsername, saveSession, saveUser, saveReset, getResetToken, deleteResetToken, addAdmin, getAdminId
from ..services.auth import generateSessionToken, hashSessionToken, AuthContext, requireUser, requireAdmin
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

class newPasswordResponse(BaseModel):
    statusCode: int
    message: str

class newPasswordRequest(BaseModel):
    oldPassword: str
    newPassword: str

@router.post("/register", response_model=UserResponse)
async def register(user: NewUser, response: Response):
    print("dsjdsdsdsdsdsd")
    #existingUser = await getUserUsername(user.username)
    #if existingUser:
        #raise HTTPException(status_code=400, detail="Username already registered")
    hash = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    hashPass = hash.decode("utf-8")
    userId = str(uuid4())
    novUser = Uporabnik(id=userId,username=user.username,email=user.email,password=hashPass)
    await saveUser(novUser)
    print("lala")

    raw = generateSessionToken()
    token = hashSessionToken(raw)
    expires = datetime.utcnow() + timedelta(days=1)
    await saveSession(Session(userId=userId, token=token,createdAt=datetime.utcnow(), expiresAt=expires, revoked=False))

    response.set_cookie(
        key="sessionId", 
        value=raw,
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

            raw = generateSessionToken()
            hashToken = hashSessionToken(raw)

            if user.remember:
                maxAge = 3600 * 24 * 7 * 30  # 1 month
            else:
                maxAge = 3600 * 24  # 1 day

            expires = datetime.utcnow() + timedelta(seconds=maxAge)

            await saveSession(Session(userId=userId, token=hashToken, createdAt=datetime.utcnow(), expiresAt=expires, revoked=False))
            
            response.set_cookie(
                key="sessionId", 
                value=raw,
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

            raw = generateSessionToken()
            hashToken = hashSessionToken(raw)

            if user.remember:
                maxAge = 3600 * 24 * 7 * 30  # 1 month
            else:
                maxAge = 3600 * 24  # 1 day

            expires = datetime.utcnow() + timedelta(seconds=maxAge)
            await saveSession(Session(userId=userId, hashToken=hashToken, expiresAt=expires, revoked=False))

            response.set_cookie(
                key="sessionId", 
                value=raw,
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
async def check(_: AuthContext = Depends(requireUser)):
    return {"loggedIn": True}
    
@router.get("/checkAdmin")
async def checkAdmin():
    return {"admin": True}
    #return {"admin": auth.isAdmin}
    #auth: AuthContext = Depends(requireAdmin)

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
async def getProfile(auth: AuthContext = Depends(requireUser)):
    userId = auth.userId
    user = await getUserId(userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username}

@router.get("/getAllUsers")
async def getAllUsers():
    return await getAllUsersDb()

@router.post("/newPassword", response_model=newPasswordResponse)
async def newPasswordRoute(auth: AuthContext = Depends(requireUser), passwords: newPasswordRequest = None):
    userId = auth.userId
    user = await getUserId(userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt.checkpw(passwords.oldPassword.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    if bcrypt.checkpw(passwords.oldPassword.encode('utf-8'), passwords.newPassword.encode('utf-8')):
        raise HTTPException(status_code=400, detail="New password cannot be the same as the old password")
    else:
        hashPass = bcrypt.hashpw(passwords.newPassword.encode('utf-8'), bcrypt.gensalt())
        user.password = hashPass.decode('utf-8')
        await saveUser(user)
        return {"statusCode": 200, "message": "Password has been changed successfully"}
        