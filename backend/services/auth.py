from datetime import datetime
from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel
import hashlib
import secrets

from ..database.creators.models import Session
from ..database.servicesDb.databaseServ import getAdminId ,getSessionHashToken, revokeSessionToken

class AuthContext(BaseModel):
    userId: str
    sessionId: str
    isAdmin: bool

def generateSessionToken():
    return secrets.token_hex(32)

def hashSessionToken(token: str):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

async def requireUser(request: Request):
    raw = request.cookies.get("sessionId")
    if not raw:
        raise HTTPException(status_code=401, detail="Unauthorized")
    hashToken = hashSessionToken(raw)
    session = await getSessionHashToken(hashToken)
    if not session or session.revoked:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if session.expiresAt < datetime.utcnow():
        await revokeSessionToken(hashToken)
        raise HTTPException(status_code=401, detail="Session expired")
    isAdmin = await getAdminId(session.userId)
    return AuthContext(userId=session.userId, sessionId=hashToken, isAdmin=isAdmin is not None)

async def requireAdmin(auth: AuthContext = Depends(requireUser)):
    if not auth.isAdmin:
        raise HTTPException(status_code=403, detail="Forbidden")
    return auth