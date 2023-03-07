from pymongo import MongoClient
from app.Configuration.configuration import logger
from app.Configuration.Helpers.tools import get_enviromental_variable


class MongoDB:
    __instance = None
    
    @staticmethod
    async def get_instance():
        try:
            if not MongoDB.__instance:
                MongoDB.__instance = MongoClient(get_enviromental_variable('MONGO_DB_SERVER'), int(get_enviromental_variable('MONGO_DB_PORT')))
            return MongoDB.__instance
        except Exception as exception:
            logger.error(f"[Initialize Database Exception]: {str(exception)}")
            
    