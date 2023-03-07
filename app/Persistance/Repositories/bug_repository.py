from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import sqlalchemy
from sqlalchemy.orm import contains_eager
from app.Core.Domain.Models.bug import Bug
from app.Configuration.configuration import logger


class BugRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str) -> Bug or None:
        try:
            bug = (await self.session.execute(select(Bug).where(Bug.id == int(id))
                                                  .outerjoin(Bug.comments)
                                                  .outerjoin(Bug.attachments)
                                                  .outerjoin(Bug.project)
                                                  .outerjoin(Bug.reporter)
                                                  .outerjoin(Bug.assignee)
                                                  .options(contains_eager(Bug.comments), contains_eager(Bug.attachments),contains_eager(Bug.project),contains_eager(Bug.reporter),contains_eager(Bug.assignee)))).scalars().first()
            return bug if bug else None
        except sqlalchemy.exc.SQLAlchemyError as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving project | {exception}")
        except Exception as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving project | {exception}")

    async def get_all(self) -> List[Bug]:
        try:
            return self.session.execute(select(Bug)).scalars().all()
        except sqlalchemy.exc.SQLAlchemyError as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving projects | {exception}")
        except Exception as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : while retrieving projects | {exception}")
