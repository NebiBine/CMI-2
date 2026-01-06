from odmantic import Model, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field as PydanticField

class Question(BaseModel):
    id: str = PydanticField(default_factory=lambda: str(uuid4()))
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
    city: str = Field(default="")
    admin_level: int = Field(default=1)  # 1 - city admin, 2 - nace in bine admin...

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

class Reward(Model):
    id: str = Field(primary_field=True, default_factory=lambda: str(uuid4()))
    name: str
    description: str
    pointsRequired: int
    imageUrl: Optional[str] = ""  # URL or path to the reward image

class UserRewards(Model):
    userId: str  # foreign key to Uporabnik
    rewardId: str  # foreign key to Reward
    claimedAt: datetime = Field(default_factory=datetime.utcnow)

class Results(Model):
    pollId: str  # foreign key to Poll
    answers: dict  # questionId -> answer