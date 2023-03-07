from sqlalchemy import Table, Column, Integer, ForeignKey,String,BIGINT
from sqlalchemy.orm import relationship
from app.Core.Domain.base_model import Base

project_user_association_table = Table(
    "project_user_association",
    Base.metadata,
    Column("project_id", BIGINT, ForeignKey("Project.id")),
    Column("user_id", BIGINT, ForeignKey("User.id")),
)