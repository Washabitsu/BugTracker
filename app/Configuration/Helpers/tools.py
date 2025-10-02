import os
from app.Configuration.configuration import logger

def get_enviromental_variable(variable_name):
    try:
        # Default values for common variables
        defaults = {
            "NAME": "Issue Tracker API",
            "API_VERSION": "1.0.0", 
            "DESCRIPTION": "Issue tracking system for the whole ecosystem",
            "API_PATH": "/api/v1",
            "SECRET_KEY": "default_secret_key_change_in_production",
            "OAUTH_USER_ENDPOINT": "https://example.com/user",
            "POSTGRES_DIALECT": "postgresql",
            "POSTGRES_DRIVER": "psycopg2",
            "POSTGRES_ASYNC_DRIVER": "asyncpg",
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "password",
            "POSTGRES_SERVER": "localhost",
            "POSTGRES_PORT": "5432",
            "POSTGRES_DB": "bugtracker",
            "POSTGRES_SHARD_ID": "1",
            "AUTO_MIGRATE_DB": "false"
        }
        
        variable = os.getenv(variable_name)
        if variable is None:
            if variable_name in defaults:
                return defaults[variable_name]
            else:
                raise ValueError(f"Couldn't retrieve variable: {variable_name}")
        return variable
    except ValueError as value_error:
        logger.error(value_error)
        return defaults.get(variable_name, "")
    except Exception as general_exception:
        logger.error(general_exception)
        return defaults.get(variable_name, "")