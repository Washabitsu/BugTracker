from fastapi import FastAPI, Header, HTTPException, APIRouter, Depends
from app.Api.authorization import get_current_user, get_admin, get_developer
from app.Core.Schemas.bug import BugCreate, BugUpdate, Bug as BugSchema
from app.Persistance.session import get_session, UnitOfWork
from app.Configuration.configuration import logger
from typing import List
from app.Core.Domain.Models.bug import Bug
from app.Core.Domain.Models.user import User
from app.Core.Domain.Enums.status import Status
from app.Core.Domain.Enums.severity import Severity
from datetime import datetime
router = APIRouter()


# READ
@router.get("/bugs/", response_model=List[BugSchema])
async def get_all(uow: UnitOfWork = Depends(get_session)):
    try:
        bug_fdb: Bug = await uow.bug_repository.get_all()
        if bug_fdb is None:
            raise HTTPException(status_code=404, detail="Bug not found")
        bug_fdb
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while retrieving bugs | {exception}")


@router.get("/bugs/{bug_id}", response_model=BugSchema)
async def get(bug_id: int, uow: UnitOfWork = Depends(get_session)):
    try:
        bug_fdb: Bug = await uow.bug_repository.get_by_id(int(bug_id))
        if bug_fdb is None:
            raise HTTPException(status_code=404, detail="Bug not found")
        return bug_fdb
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while editing bug with id {bug_id} | {exception}")

# CREATE


@router.post("/bugs/")
async def create(bug: BugCreate, user=Depends(get_current_user), uow: UnitOfWork = Depends(get_session)):
    try:
        project = await uow.project_repository.get_by_id(bug.project_id)
        if project is None:
            raise HTTPException(404,"Project not found!")
        
        new_bug = Bug(
            title=bug.title,
            description=bug.description,
            status=Status.NEW,
            severity=bug.severity,
            date_reported=datetime.now(),
            reporter=user
        )
        await uow.add(new_bug)
        await uow.commit()
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while creating bug | {exception}")


# UPDATE
@router.put("/bugs/{bug_id}")
async def edit(bug_id: str, bug: BugUpdate, user_id: str = None, username=Depends(get_admin), uow: UnitOfWork = Depends(get_session)):
    try:
        bug_fdb: Bug = await uow.bug_repository.get_by_id(int(bug_id))
        if bug is None:
            raise HTTPException(status_code=404, detail="Bug not found")
        else:
            await bug_fdb.update(bug)
            if user_id is not None:
                user: User = await uow.user_repository.get_by_id(user_id)
                if user is None:
                    raise HTTPException(
                        404, "User could not be found with that id!")
                else:
                    bug_fdb.assign(user)
            await uow.mark_dirty(bug)
            await uow.commit()
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while editing bug with id {bug_id} | {exception}")


@router.delete("/bugs/{bug_id}")
async def delete(bug_id: str, username=Depends(get_admin), uow: UnitOfWork = Depends(get_session)):
    try:
        bug = await uow.bug_repository.get_by_id(int(bug_id))
        if bug is None:
            raise HTTPException(status_code=404, detail="Bug not found")
        else:
            await uow.mark_deleted(bug)
            await uow.commit()
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while deleting bug with id {bug_id} | {exception}")
