from app.Core.Domain.base_model import Base
from sqlalchemy import BIGINT, Boolean, Column, DateTime, ForeignKey, String, func, text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from app.Core.Domain.Enums.roles import Roles
from app.Core.Domain.Models.project_user import project_user_association_table

class User(Base):
    __tablename__ = "User"
    
    id = Column(
        BIGINT, primary_key=True, server_default=text("generate_snowflake_id()")
    )
    
    username = Column(String, nullable=False,unique=True)
    email = Column(String(255),nullable=False,unique=True)
    phone = Column(String(20),nullable=True)
    role = Column(ENUM(Roles,name="roles"),nullable=False)
    
    date_created = Column(DateTime,nullable=False, server_default=func.now())
    comments = relationship("Comment",backref="User")
    notifications = relationship("Notification",backref="User")
    reported_bugs = relationship('Bug', foreign_keys='Bug.reporter_id', back_populates='reporter')
    assigned_bugs = relationship('Bug',  foreign_keys='Bug.assignee_id',back_populates='assignee')
    projects = relationship("Project", secondary=project_user_association_table, back_populates='users', viewonly=True)