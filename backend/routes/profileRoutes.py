from fastapi import APIRouter, Depends, HTTPException, Response, Request, File, UploadFile, Form
from pydantic import BaseModel
import os
import aiofiles
import base64
import sys

from ..database.creators.models import Admins, Cities, Uporabnik, Profile
from ..database.servicesDb.databaseServ import deleteCity, getAllCities, saveCity, createProfile as saveProfile, deleteAdmin, getProfileId, getAdminId, addAdmin

router = APIRouter()

class ProfileResponse(BaseModel):
    statusCode: int
    message: str

class getProfileResponse(BaseModel):
    statusCode: int
    message: str
    profile: Profile
    admin: bool

class ProfileRequest(BaseModel):
    userId: str

class updateProfileRequest(BaseModel):
    id: str
    first_name: str
    last_name: str
    birthdate: str
    phone: str
    address: str
    city: str
    country: str
    isAdmin: bool

@router.post("/createProfile", response_model=ProfileResponse)
async def createProfile_endpoint(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    bio: str = Form(""),
    birthdate: str = Form(""),
    phone: str = Form(""),
    address: str = Form(""),
    city: str = Form(""),
    country: str = Form(""),
    profilePicture: UploadFile = File(None),
    ):
    print("All cookies:", request.cookies, flush=True)
    userId = request.cookies.get("sessionId")
    print("Session ID:", userId, flush=True)
    if not userId:
        return {"statusCode": 500, "message": "Profile created not successfully, no userId"}
        #raise HTTPException(status_code=401, detail="Unauthorized, ni idja")
    
    pfpDir = "database/data/pfp/"
    os.makedirs(pfpDir, exist_ok=True)
    pfpSave = "database/data/pfp/default_profile_pic.png"

    if profilePicture != File(None):
        try:
            pfpDir = "database/data/pfp/"
            os.makedirs(pfpDir, exist_ok=True)
            extension = os.path.splitext(profilePicture.filename)[1]
            pfpName = f"pfp{userId}{extension}"
            pfpPath = os.path.join(pfpDir, pfpName)
            async with aiofiles.open(pfpPath, "wb") as f:
                content = await profilePicture.read()
                await f.write(content)
            pfpSave= pfpPath.replace("\\", "/")
        except Exception as e:
            return {"statusCode": 500, "message": "Profile created not successfully, no userId"}
            #raise HTTPException(status_code=500, detail="Failed to save profile picture")
    
    profile = Profile(
        id=userId,
        first_name=first_name,
        last_name=last_name,
        bio=bio,
        birthdate=birthdate,
        phone=phone,
        address=address,
        city=city,
        country=country,
        profile_picture_url=pfpSave,
    )
    await saveProfile(profile)
    await saveCity(Cities(city=city))
    return {"statusCode": 200, "message": "Profile created successfully backend"}

@router.post("/getProfile", response_model=getProfileResponse)
async def getProfile(user: ProfileRequest):
    profile =  await getProfileId(user.userId)
    isAdmibBool = False
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    isAdmin = await getAdminId(user.userId)
    if isAdmin:
        isAdmibBool = True
    return {"statusCode": 200, "message": "Profile fetched successfully", "profile": profile, "admin": isAdmibBool} # dodej za admin level

@router.post("/updateProfile", response_model=ProfileResponse)
async def updateProfile(profile: updateProfileRequest):
    existingProfile = await getProfileId(profile.id)
    if not existingProfile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    existingProfile.first_name = profile.first_name
    existingProfile.last_name = profile.last_name
    existingProfile.birthdate = profile.birthdate
    existingProfile.phone = profile.phone
    existingProfile.address = profile.address
    existingProfile.city = profile.city
    existingProfile.country = profile.country

    await saveProfile(existingProfile)
    allCities = await getAllCities()
    if profile.city not in allCities:
        await saveCity(Cities(city=profile.city))


    admin = await getAdminId(profile.id)
    if profile.isAdmin and not admin:
        newAdmin = Admins(
            id=profile.id,
            city=profile.city,
            admin_level=1
        )
        await addAdmin(newAdmin)
    elif not profile.isAdmin and admin:
        await deleteAdmin(admin)

    return {"statusCode": 200, "message": "Profile updated successfully"}

    