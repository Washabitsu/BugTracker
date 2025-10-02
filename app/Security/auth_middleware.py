

import json
from time import time
from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from app.Core.Domain.Enums import status
from app.Core.Domain.Enums.roles import Roles
from app.Core.Domain.Models.user import User
from app.Persistance.session import get_session
from app.Security.jwt_handler import JWTHandler

async def AuthMiddleware(request: Request, call_next):
    # Allow CORS preflight requests to pass through
    if request.method == "OPTIONS":
        return await call_next(request)

    headers = request.headers.get("Authorization")
    [token_type, token] = headers.split(" ") if headers else (None, None)
    if token_type != "Bearer" or not token:
        return JSONResponse({"detail": "Invalid or missing token"}, status_code=401)

    verify = JWTHandler().verify_token(token)

    if verify is None:
        return JSONResponse({"detail": "Invalid token"}, status_code=401)

    request.state.user = verify

    response = await call_next(request)
    return response


async def get_current_user(request: Request, session=Depends(get_session)):
    user = getattr(request.state, "user", None)
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
    
    token_sub = user.get("sub")
    
    if not token_sub:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    db_user = await session.user_repository.get_by_username(token_sub)

    if db_user == None: 
        new_user = User(username=token_sub, email=user.get("email"), role=Roles.DEVELOPER)
        await session.add(new_user)
        await session.commit()
        return new_user
    return db_user