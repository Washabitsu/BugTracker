from enum import auto
from sqlalchemy.future.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import NullPool
import os
from app.Configuration.Helpers.tools import get_enviromental_variable


def get_database_connection_string(is_async: bool = True) -> str:
    return "{0}+{1}://{2}:{3}@{4}:{5}/{6}".format(
        get_enviromental_variable('POSTGRES_DIALECT'),
        get_enviromental_variable('POSTGRES_ASYNC_DRIVER')
        if is_async
        else get_enviromental_variable('POSTGRES_DRIVER'),
        get_enviromental_variable('POSTGRES_USER'),
        get_enviromental_variable('POSTGRES_PASSWORD'),
        get_enviromental_variable('POSTGRES_SERVER'),
        get_enviromental_variable('POSTGRES_PORT'),
        get_enviromental_variable('POSTGRES_DB')
    )
    
def get_database_connection_string_raw(is_async: bool = True) -> str:
    return "{0}+{1}://{2}:{3}@{4}:{5}".format(
        get_enviromental_variable('POSTGRES_DIALECT'),
        get_enviromental_variable('POSTGRES_ASYNC_DRIVER')
        if is_async
        else get_enviromental_variable('POSTGRES_DRIVER'),
        get_enviromental_variable('POSTGRES_USER'),
        get_enviromental_variable('POSTGRES_PASSWORD'),
        get_enviromental_variable('POSTGRES_SERVER'),
        get_enviromental_variable('POSTGRES_PORT')
    )


def create_database_engine(is_async: bool = True) -> AsyncEngine or Engine:
    return (
        # poolclass=NullPool is required, in order to execute multi-threading async SQL operations.
        create_async_engine(
            get_database_connection_string(is_async=is_async),
            poolclass=NullPool,
            pool_pre_ping=True,
            echo=False,
        )
        if is_async
        else create_engine(
            get_database_connection_string(is_async=is_async), echo=False
        )
    )


def create_database_session(engine: AsyncEngine) -> AsyncSession:
    return AsyncSession(
        bind=engine,
        expire_on_commit=False,
    )


def create_database_sessionmaker(engine: AsyncEngine or Engine) -> AsyncSession or Session:
    return sessionmaker(
        bind=engine,
        class_=AsyncSession if type(engine) == AsyncEngine else Engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

