from sqlalchemy.future.engine import Engine
from sqlalchemy.orm.session import Session, sessionmaker
from app.Persistance.database import (
    create_database_engine,
    create_database_sessionmaker,
    create_database_session
)
from app.Persistance.unit_of_work import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

# Create engine and session for our database connection, through the API routes.
local_engine: AsyncEngine = create_database_engine()
local_sync_engine : Engine = create_database_engine(False)
local_session_maker: sessionmaker = create_database_sessionmaker(engine=local_engine)
sync_local_session_maker : sessionmaker = create_database_sessionmaker(local_sync_engine)
local_session: AsyncSession = create_database_session(engine=local_engine)

# Dependency for getting the database session.
async def get_session() -> UnitOfWork:
    try:
        async with local_session_maker() as session:
            yield UnitOfWork(session)
    finally:
        if session:
            await session.close()

