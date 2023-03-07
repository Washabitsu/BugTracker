from app.Core.Domain.base_model import Base
from sqlalchemy import BIGINT, Boolean, Column, DateTime, ForeignKey, String, func, text,Date
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base, relationship
from app.Core.Domain.Enums.roles import Roles
from app.Core.Domain.Models.project_user import project_user_association_table

class Project(Base):
    __tablename__ = "Project"
    
    id = Column(
        BIGINT, primary_key=True, server_default=text("generate_snowflake_id()")
    )
    
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(Date,nullable=False)
    end_date = Column(Date,nullable=False)
    
    users = relationship("User", secondary=project_user_association_table, back_populates='projects')
    bugs = relationship("Bug",foreign_keys="Bug.project_id",back_populates="project")
    
    async def update(self,project,users):
        self.name = project.name if project.name else self.name
        self.description = project.description if project.description else self.description
        self.start_date = project.start_date if project.start_date else self.start_date
        self.end_date = project.end_date if project.end_date else self.end_date
        self.users = users if users else self.users