from odmantic import Model, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Question(BaseModel):
    text: str
    type: str
    options: list[str]

class Uporabnik(Model):
    id: str = Field(primary_field=True, default_factory=lambda: str(uuid4()))
    email: str
    username: str
    password: str


class Profile(Model):
    id: str = Field(primary_field=True)  # same id as the userId cookie
    first_name: str
    last_name: str
    bio: Optional[str] = ""
    birthdate: Optional[str] = ""  # or use date if you want strict typing
    phone: Optional[str] = ""
    address: Optional[str] = ""
    city: Optional[str] = ""
    country: Optional[str] = ""
    profile_picture_url: str
    #profile_picture_url: str = "database/data/pfp/default_profile_pic.png"

class Admins(Model):
    id: str = Field(primary_field=True)
    city: str = ""
    admin_level: int = 1  # 1 - city admin, 2 - nace in bine admin...

class Reset(Model):
    id: str = Field(primary_field=True, default_factory=lambda: str(uuid4()))
    userId: str  # foreign key to Uporabnik
    token: str  # unique reset token
    expiry: datetime  # token expiry time

class Poll(Model):
    id: str = Field(primary_field=True, default_factory=lambda: str(uuid4()))
    creatorId: str  # foreign key to Uporabnik
    city: str
    pollTitle: str
    pollDuration: int  # in days
    expirationDate: datetime
    creationDate: datetime = Field(default_factory=datetime.utcnow)
    points: int
    questions: list[Question]  # each question can be represented as a dicts