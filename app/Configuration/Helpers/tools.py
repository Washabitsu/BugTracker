import os
from app.Configuration.configuration import logger

def get_enviromental_variable(variable_name):
    try:
        variable = os.getenv(variable_name)
        if variable is None:
            raise ValueError("Couldn't retrieve variable!")
        return variable
    except ValueError as value_error:
        logger.error(value_error)
    except Exception as general_exception:
        logger.error(general_exception)