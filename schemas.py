# schemas.py

from pydantic import BaseModel
from typing import List, Optional
from models import (
    BadgeTypeEnum,
    TaskBadgeTypeEnum,
)

class Interest(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class BadgeData(BaseModel):
    badgeType: BadgeTypeEnum
    count: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: Optional[str]
    profile: Optional[str]
    interest: Optional[Interest]  # 수정됨

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    badgeData: List['BadgeData'] = []

    class Config:
        from_attributes = True

class MentoringStatusRead(BaseModel):
    id: int
    name: str
    interest: Optional[Interest]  # 수정됨
    status: str
    badgeData: List[BadgeData] = []

    class Config:
        from_attributes = True

class UserMentoringData(BaseModel):
    id: int
    name: str
    mentoring: str  # "멘토" 또는 "멘티"
    badgeData: List[BadgeData] = []
    email: Optional[str]

    class Config:
        from_attributes = True

class TaskData(BaseModel):
    id: int
    image: str
    company: str
    title: str
    description: str
    badgeType: TaskBadgeTypeEnum

    class Config:
        from_attributes = True

BadgeData.update_forward_refs()
UserRead.update_forward_refs()
MentoringStatusRead.update_forward_refs()
