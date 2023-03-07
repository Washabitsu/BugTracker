from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
from app.Core.Schemas.user import UserOut
from app.Core.Schemas.bug import Bug


class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    users_ids: List[str] = []


class ProjectUpdate(ProjectBase):
    users_ids: List[str] = []


class Project(ProjectBase):
    id: Optional[int] = None
    users: Optional[List[UserOut]] = []
    bugs: Optional[List[Bug]] = []

    @validator('id', pre=True)
    def id_to_str(cls, v):
        return str(v)

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
