# from app.api.dependencies import get_current_active_user

from fastapi import APIRouter
from app.Api.authorization import router as oauth_router
from app.Api.Endpoints.project import router as project_router
from app.Api.Endpoints.bug import router as bug_router
# dependencies = [Depends(get_current_active_user)]

api_router = APIRouter()

api_router.include_router(oauth_router, tags=["OAuth Authentication for mitchoulious identity server"])
api_router.include_router(project_router, tags=["Project"])
api_router.include_router(bug_router, tags=["Bug"])



