from app.Core.Domain.base_model import Base
from sqlalchemy import BIGINT, Boolean, Column, DateTime, ForeignKey, String, func, text,Date
from sqlalchemy.dialects.postgresql import ENUM,BYTEA
from sqlalchemy.orm import declarative_base, relationship
from app.Core.Domain.Enums.roles import Roles


class Attachment(Base):
    __tablename__ = "Attachment"
    
    id = Column(
        BIGINT, primary_key=True, server_default=text("generate_snowflake_id()")
    )
    
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    size = Column(BIGINT,ForeignKey('User.id'))
    mongodb_id = Column(BYTEA(12),nullable=False)
    
    comment_id = Column(BIGINT,ForeignKey('Comment.id'))
    issue_id = Column(BIGINT,ForeignKey('Issue.id'))