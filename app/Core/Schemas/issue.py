from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator
from app.Core.Domain.Enums.severity import Severity
from app.Core.Domain.Enums.status import Status
from app.Core.Domain.Enums.issue_type import IssueTypeStr

class IssueBase(BaseModel):
    title: str
    description: str
    severity: Severity
    project_id: int
    reporter_id: int
    issue_type: IssueTypeStr

    @validator('reporter_id','project_id', pre=True)
    def id_to_str(cls, v):
        return str(v)

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

class IssueCreate(IssueBase):
    pass

class IssueUpdate(IssueBase):
    status: Status
    assignee_id: Optional[int] = None
    date_resolved: Optional[datetime] = None
    
    @validator('assignee_id', pre=True)
    def id_to_str(cls, v):
        return str(v)

class Issue(IssueBase):
    id: int
    status: Optional[Status] = None
    assignee_id: Optional[int] = None
    date_reported: Optional[datetime] = None
    date_resolved: Optional[datetime] = None
    @validator('id', 'assignee_id', pre=True)
    def id_to_str(cls, v):
        return str(v)
