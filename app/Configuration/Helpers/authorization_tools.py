import jwt
from datetime import datetime, timedelta
from app.Configuration.Helpers.tools import get_enviromental_variable
from app.Core.Domain.Models.user import User
from app.Configuration.configuration import logger

async def create_jwt_token(user: User):
    try:
        expiration_date = datetime.now() + timedelta(minutes=int(get_enviromental_variable(
                'ACCESS_TOKEN_EXPIRATION_MINUTES')))
        payload = {"sub": user.username, "role": user.role,
                   "expiration_date": expiration_date.strftime("%m/%d/%YT%H:%M:%S")}
        jwt_token = jwt.encode(payload, get_enviromental_variable(
            'SECRET_KEY'), algorithm="HS256")
        return {"token": jwt_token, "exp_date": expiration_date.strftime("%m/%d/%YT%H:%M:%S")}
    except Exception as exception:
        logger.error(f"[JWT Token Exception] : exception occured while generating jwt key | {exception}")
