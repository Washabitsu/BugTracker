from app.Core.Domain.base_model import Base
from sqlalchemy import BIGINT, Boolean, Column, DateTime, ForeignKey, String, func, text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base, relationship
from app.Core.Domain.Enums.roles import Roles


class Comment(Base):
    __tablename__ = "Comment"
    
    id = Column(
        BIGINT, primary_key=True, server_default=text("generate_snowflake_id()")
    )
    
    comment = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_created = Column(DateTime,nullable=False)  
    
    user_id = Column(BIGINT,ForeignKey('User.id'))
    issue_id = Column(BIGINT,ForeignKey('Issue.id'))
    
    attachments = relationship("Attachment",backref="Comment")