from sqlalchemy.future.engine import Engine
from app.Configuration.Helpers.tools import get_enviromental_variable
from app.Persistance.database_queries import get_snowflake_id_generator_queries
from sqlalchemy import create_engine, exc
from app.Core.Domain.base_model import Base
from app.Persistance.database import create_database_engine, get_database_connection_string_raw
from sqlalchemy.sql.expression import text
from pymongo import MongoClient
import logging


logger = logging.getLogger(__name__)


def create_database():
    try:
        engine = create_engine(
            get_database_connection_string_raw(False), 
            isolation_level="AUTOCOMMIT"
        )
        
        with engine.connect() as connection:
            database = connection.execute(text("SELECT datname  FROM pg_database;")).scalars().all()
            db_name = get_enviromental_variable("POSTGRES_DB")
            if db_name not in database:
                connection.execute(text(f"CREATE DATABASE {db_name};"))

    except exc.SQLAlchemyError as sqlalchemy_exception:
        logger.error(
            f"[Initialize Database SQLAlchemyError]: {sqlalchemy_exception._message()}"
        )
    except Exception as exception:
        logger.error(f"[Initialize Database Exception]: {str(exception)}")
    finally:
        # Close and dispose engine for now.
        if engine:
            engine.dispose()
            

def initialize_database():
    try:
        create_database()
        # Create new synchronous engine each time, to avoid confliction.
        engine = create_database_engine(is_async=False)

        # Create the needed functions and sequences for the snowflake ids.
        if create_snowflake_id_generator(engine=engine):

            # noqa (No Quality Assurance) for the linter, specific for rule F401.
            from app.Core.Domain import base  # noqa: F401
        
            # Create all the ORM models, if any is missing.
            Base.metadata.create_all(engine)
    except exc.SQLAlchemyError as sqlalchemy_exception:
        logger.error(
            f"[Initialize Database SQLAlchemyError]: {sqlalchemy_exception._message()}"
        )
    except Exception as exception:
        logger.error(f"[Initialize Database Exception]: {str(exception)}")
    finally:
        # Close and dispose engine for now.
        if engine:
            engine.dispose()
        
def create_snowflake_id_generator(engine: Engine) -> bool:
    try:
        with engine.connect() as connection:            
            [connection.execute(query) for query in get_snowflake_id_generator_queries()]
            connection.commit()
        return True
    except exc.SQLAlchemyError as sqlalchemy_exception:
        logger.error(
            f"[Create Snowflake ID Generator SQLAlchemyError]: {sqlalchemy_exception._message()}"
        )
        return False
    except Exception as exception:
        logger.error(f"[Create Snowflake ID Generator Exception]: {str(exception)}")
        return False


if __name__ == "__main__":
    initialize_database()
