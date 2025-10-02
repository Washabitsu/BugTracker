from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import sqlalchemy
from sqlalchemy.orm import contains_eager
from app.Core.Domain.Models.issue import Issue
from app.Configuration.configuration import logger


class IssueRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str) -> Optional[Issue]:
        try:
            issue = (await self.session.execute(select(Issue).where(Issue.id == int(id))
                                                  .outerjoin(Issue.comments)
                                                  .outerjoin(Issue.attachments)
                                                  .outerjoin(Issue.project)
                                                  .outerjoin(Issue.reporter)
                                                  .outerjoin(Issue.assignee)
                                                  .options(contains_eager(Issue.comments), contains_eager(Issue.attachments),contains_eager(Issue.project),contains_eager(Issue.reporter),contains_eager(Issue.assignee)))).scalars().first()
            return issue if issue else None
        except sqlalchemy.exc.SQLAlchemyError as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving project | {exception}")
        except Exception as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving project | {exception}")

    async def get_all(self) -> List[Issue]:
        try:
            return self.session.execute(select(Issue)).scalars().all()
        except sqlalchemy.exc.SQLAlchemyError as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving projects | {exception}")
        except Exception as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : while retrieving projects | {exception}")