from typing import List
from fastapi import FastAPI, Header, HTTPException, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.Core.Domain.Models.user import User
from app.Persistance.session import get_session
from app.Persistance.unit_of_work import UnitOfWork
from app.Core.Domain.Models.mongo_db import MongoDB
from app.Core.Domain.Enums.roles import Roles
import jwt
import requests
import json
from app.Persistance.session import local_session_maker
from app.Configuration.Helpers.tools import get_enviromental_variable
from app.Configuration.Helpers.authorization_tools import create_jwt_token


async def get_current_user(token: str = Header(None)):
    await authenticate_jwt(token,[Roles.TESTER,Roles.ADMINISTRATOR,Roles.DEVELOPER])

async def get_admin(token: str = Header(None)):
    await authenticate_jwt(token,[Roles.ADMINISTRATOR])

async def get_developer(token: str = Header(None)):
    await authenticate_jwt(token,[Roles.DEVELOPER])
    
async def authenticate_jwt(token: str,roles:List[Roles]):
    if not token:
            raise HTTPException(
                status_code=401, detail="Missing authorization header")
    try:
        payload = jwt.decode(token, get_enviromental_variable(
                'SECRET_KEY'), algorithms=["HS256"])
        username = payload.get("sub")
        jwt_role = payload.get("role")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        if Roles(jwt_role) not in roles:
            raise HTTPException(status_code=401, detail="You are not authorized to access this resource!") 
        
        async with local_session_maker() as session:
            uow = UnitOfWork(session)
            
            return await uow.user_repository.get_by_username(username)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def hasUserRights(user:User,users:List[User]):
    does_exist = False
    for _user in users:
        if user.username == _user.username:
            does_exist = True
            break
    return does_exist

router = APIRouter()


@router.post("/oauth")
async def oauth_server(token: str = Header(None), uow: UnitOfWork = Depends(get_session)):
    try:
        if not token:
            raise HTTPException(
                status_code=401, detail="Missing authorization header")

        url = get_enviromental_variable("OAUTH_USER_ENDPOINT")

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", url, headers=headers, verify=False)

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid token")

        if response.status_code == 200:
            retrieved_data = json.loads(response.text)

            user = await uow.user_repository.get_by_username(retrieved_data["username"])
            client = await MongoDB.get_instance()
            db = client['BugTrackerFiles']
            if user is None:
                user = User(
                    username=retrieved_data["username"],
                    email=retrieved_data["email"],
                    phone=retrieved_data["phoneNumber"],
                    role= Roles.DEVELOPER
                )
                await uow.add(user)
                await uow.commit()
            jwt_token = await create_jwt_token(user)
            return jwt_token
    except Exception as exception:

        raise exception
