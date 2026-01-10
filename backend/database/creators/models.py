from odmantic import Model, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field as PydanticField

class Question(BaseModel):
    id: str = PydanticField(default_factory=lambda: str(uuid4()))
    text: str
    type: str
    options: list[str]

class Option(BaseModel):
    optionText: str
    result: list[Union[int, str]] = []

class QuestionResult(BaseModel):
    questionId: str
    questionType: str
    questionText: str
    option1 : Option
    option2 : Option
    option3 : Option
    option4 : Option

class Results(Model):
    id: str = Field(primary_field=True, default_factory=lambda: str(uuid4()))
    pollId: str  # foreign key to Poll
    answers: dict[str, QuestionResult]

"""
dict structure for answers:
{
    questionId1: {
        questionId: str
        questionType: str
        option1 : Option
        option2 : Option
        option3 : Option
        option4 : Option ----> samo QuestionResult
    },
    questionId2: {
        questionId: str
        questionType: str
        option1 : Option
        option2 : Option
        option3 : Option
        option4 : Option ----> samo QuestionResult
    }
}
"""

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
    pollDescription: str
    pollDuration: int  # in days
    expirationDate: datetime
    creationDate: datetime = Field(default_factory=datetime.utcnow)
    points: int
    questions: list[Question]  # each question can be represented as a dicts
    
class PollArchive(Model):
    id: str = Field(primary_field=True, default_factory=lambda: str(uuid4()))
    creatorId: str  # foreign key to Uporabnik
    city: str
    pollTitle: str
    pollDescription: str
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

class UserPoints(Model):
    userId: str  # foreign key to Uporabnik
    points: int = Field(default=0)
    completedPolls: list[str] = []