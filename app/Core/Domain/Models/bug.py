from app.Core.Domain.base_model import Base
from sqlalchemy import BIGINT, Boolean, Column, DateTime, ForeignKey, String, func, text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from app.Core.Domain.Enums.status import Status
from app.Core.Domain.Enums.severity import Severity
from app.Core.Schemas.bug import BugUpdate

class Bug(Base):
    __tablename__ = "Bug"
    
    id = Column(
        BIGINT, primary_key=True, server_default=text("generate_snowflake_id()")
    )
    
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(ENUM(Status,name="status"),nullable=False)
    severity = Column(ENUM(Severity,name="severity"),nullable=False)
    date_reported = Column(DateTime,nullable=False, server_default=func.now())
    date_resolved = Column(DateTime,nullable=True)
    
    project_id = Column(BIGINT,ForeignKey('Project.id'))
    reporter_id = Column(BIGINT, ForeignKey('User.id'))
    assignee_id = Column(BIGINT, ForeignKey('User.id'))


    project = relationship('Project', foreign_keys=[project_id])
    reporter = relationship('User', foreign_keys=[reporter_id])
    assignee = relationship('User', foreign_keys=[assignee_id])
    
    comments = relationship("Comment",backref="Bug")
    attachments = relationship("Attachment",backref="Bug")
    
    
    async def update(self,bug:BugUpdate):
        self.title = bug.title if bug.title else self.title
        self.description = bug.description if bug.description else self.description
        self.status = bug.status if bug.status else self.status
        self.severity = bug.severity if bug.severity else self.severity
        self.date_resolved = bug.date_resolved if bug.date_resolved else self.date_resolved
    
    async def assign(self,user):
        self.assignee = user