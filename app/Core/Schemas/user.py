from typing import List, Optional
from pydantic import BaseModel, validator
from app.Core.Schemas.issue import Issue


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str]


class UserOut(UserBase):
    id: int

    @validator('id', pre=True)
    def id_to_str(cls, v):
        return str(v)

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    issues_reported: List[Issue] = []
    issues_assigned: List[Issue] = []

    @validator('id', pre=True)
    def id_to_str(cls, v):
        return str(v)

    class Config:
        orm_mode = True
