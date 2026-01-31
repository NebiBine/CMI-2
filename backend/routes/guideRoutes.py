from fastapi import APIRouter, HTTPException, Response, Request, Form
from pydantic import BaseModel

router = APIRouter()

@router.post("/test")
async def testRoute(request: Request):
    return {"message": "This is a test route"}