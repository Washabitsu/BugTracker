from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import sqlalchemy
from app.Core.Domain.Models.user import User
from app.Configuration.configuration import logger


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> User or None:
        try:
            user = (await self.session.execute(select(User).where(User.username == username))).scalars().first()
            return user if user else None
        except sqlalchemy.exc.SQLAlchemyError as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving user | {exception}")
        except Exception as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving user | {exception}")

    async def get_by_ids(self, ids: List[str]):
        try:
            int_ids = []
            for id in ids:
                int_ids.append(int(id))

            users = (await self.session.execute(select(User).where(User.id.in_(int_ids)))).scalars().all()
            return users if users else []
        except sqlalchemy.exc.SQLAlchemyError as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving user | {exception}")
        except Exception as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving user | {exception}")

    async def get_by_id(self, id: str) -> User or None:
        try:
            user = (await self.session.execute(select(User).where(User.id == int(id)))).scalars().first()
            return user if user else None
        except sqlalchemy.exc.SQLAlchemyError as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving user | {exception}")
        except Exception as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving user | {exception}")

    async def get_all(self) -> List[User]:
        try:
            return self.session.execute(select(User)).scalars().all()
        except sqlalchemy.exc.SQLAlchemyError as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : While retrieving users | {exception}")
        except Exception as exception:
            logger.error(
                f"[SQLAlchemy Exception Occured] : while retrieving users | {exception}")
