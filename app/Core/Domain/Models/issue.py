from app.Core.Domain.base_model import Base
from sqlalchemy import BIGINT, Boolean, Column, DateTime, ForeignKey, String, func, text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from app.Core.Domain.Enums.status import Status
from app.Core.Domain.Enums.severity import Severity
from app.Core.Domain.Enums.issue_type import IssueTypeStr
from app.Core.Schemas.issue import IssueUpdate

class Issue(Base):
    __tablename__ = "Issue"

    id = Column(
        BIGINT, primary_key=True, server_default=text("generate_snowflake_id()")
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(ENUM(Status,name="status"),nullable=False)
    severity = Column(ENUM(Severity,name="severity"),nullable=False)
    issue_type = Column(ENUM(IssueTypeStr, name="issue_type"), nullable=False)
    date_reported = Column(DateTime,nullable=False, server_default=func.now())
    date_resolved = Column(DateTime,nullable=True)
    project_id = Column(BIGINT,ForeignKey('Project.id'))
    reporter_id = Column(BIGINT, ForeignKey('User.id'))
    assignee_id = Column(BIGINT, ForeignKey('User.id'))

    project = relationship('Project', foreign_keys=[project_id])
    reporter = relationship('User', foreign_keys=[reporter_id])
    assignee = relationship('User', foreign_keys=[assignee_id])
    comments = relationship("Comment",backref="Issue")
    attachments = relationship("Attachment",backref="Issue")

    async def update(self,issue:IssueUpdate):
        self.title = issue.title if issue.title else self.title
        self.description = issue.description if issue.description else self.description
        self.status = issue.status if issue.status else self.status
        self.severity = issue.severity if issue.severity else self.severity
        self.issue_type = issue.issue_type if issue.issue_type else self.issue_type
        self.date_resolved = issue.date_resolved if issue.date_resolved else self.date_resolved

    async def assign(self,user):
        self.assignee = user