from app.Core.Domain.base_model import Base
from sqlalchemy import BIGINT, Boolean, Column, DateTime, ForeignKey, String, func, text,Date
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base, relationship
from app.Core.Domain.Enums.roles import Roles


class Notification(Base):
    __tablename__ = "Notification"
    
    id = Column(
        BIGINT, primary_key=True, server_default=text("generate_snowflake_id()")
    )
    
    text = Column(String, nullable=False)
    date_created = Column(String, nullable=False)
    users_id = Column(BIGINT,ForeignKey('User.id'))