# from app.api.dependencies import get_current_active_user

from fastapi import APIRouter
from app.Api.Endpoints.project import router as project_router
from app.Api.Endpoints.issue import router as issue_router
# dependencies = [Depends(get_current_active_user)]

api_router = APIRouter()

api_router.include_router(project_router, tags=["Project"])
api_router.include_router(issue_router, tags=["Issue"])



