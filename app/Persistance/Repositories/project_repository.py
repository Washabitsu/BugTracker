from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import sqlalchemy
from sqlalchemy.orm import contains_eager
from app.Core.Domain.Models.project import Project
from app.Configuration.configuration import logger
from app.Core.Domain.Models.user import User


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str, user: User) -> Project or None:
        try:
            project = (await self.session.execute(select(Project).where(Project.id == int(id))
                                                  .outerjoin(Project.users)
                                                  .outerjoin(Project.issues)
                                                  .where(Project.users.any(id=user.id))
                                                  .options(contains_eager(Project.users), contains_eager(Project.issues)))).scalars().first()
            return project if project else None
        except sqlalchemy.exc.SQLAlchemyError as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving project | {exception}")
        except Exception as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving project | {exception}")

    async def get_all(self, user: User) -> List[Project]:
        try:
            return (await self.session.execute(select(Project) .outerjoin(Project.users)
                                               .outerjoin(Project.issues)
                                               .where(Project.users.any(id=user.id))
                                               .options(contains_eager(Project.users), contains_eager(Project.issues)))).unique().scalars().all()
        except sqlalchemy.exc.SQLAlchemyError as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving projects | {exception}")
        except Exception as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : while retrieving projects | {exception}")
