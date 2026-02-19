import mimetypes
from fastapi import APIRouter, Depends, HTTPException, Response, Request, File, UploadFile, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import aiofiles
import base64
import sys

from backend.services.auth import AuthContext, requireUser

from ..database.creators.models import Admins, Cities, Uporabnik, Profile
from ..database.servicesDb.databaseServ import getUserId, deleteCity, getAllCities, saveCity, createProfile as saveProfile, deleteAdmin, getProfileId, getAdminId, addAdmin

router = APIRouter()

class ProfileResponse(BaseModel):
    statusCode: int
    message: str

class getProfileResponse(BaseModel):
    statusCode: int
    message: str
    profile: Profile
    admin: bool
    pfp:str
    username: str
    email: str

class ProfileRequest(BaseModel):
    userId: str
    type: int

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
    type: int

@router.post("/createProfile", response_model=ProfileResponse)
async def createProfile_endpoint(
    auth: AuthContext = Depends(requireUser),
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
    userId = auth.userId
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

@router.get("/pfp/{userId}",name="get_profile_picture")
async def uploadProfilePicture(userId: str, auth: AuthContext = Depends(requireUser)):
    userId = auth.userId
    profile = await getProfileId(userId)
    if not userId:
        raise HTTPException(status_code=401, detail="Unauthorized, no session ID")
    default_path = "database/data/pfp/default_profile_pic.png"
    path = default_path
    if profile and profile.profile_picture_url:
        path = profile.profile_picture_url

    media_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
    
    return FileResponse(path, media_type=media_type)



@router.post("/getProfile", response_model=getProfileResponse)
async def getProfile(request: Request, user: ProfileRequest, auth: AuthContext = Depends(requireUser)):
    userId = auth.userId
    if user.type != 1:
        ids = userId
    else:
        ids = userId
    profile = await getProfileId(ids)
    isAdmibBool = False
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    isAdmin = await getAdminId(ids)
    if isAdmin:
        isAdmibBool = True

    
    uporabnik = await getUserId(ids)
        

    pfp_url = str(request.url_for("get_profile_picture", userId=ids))
    
    return {"statusCode": 200, "message": "Profile fetched successfully", "profile": profile, "admin": isAdmibBool, "pfp": pfp_url, "username": uporabnik.username, "email": uporabnik.email} # dodej za admin level

@router.post("/updateProfile", response_model=ProfileResponse)
async def updateProfile(auth: AuthContext = Depends(requireUser), profile: updateProfileRequest = None):
    userId = auth.userId
    if profile.type != 1:
        ids = userId
    else:
        ids = profile.id
    existingProfile = await getProfileId(ids)
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

    if profile.type == 1:
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

    