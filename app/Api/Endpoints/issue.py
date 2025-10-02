from fastapi import FastAPI, Header, HTTPException, APIRouter, Depends
from app.Core.Schemas.issue import IssueCreate, IssueUpdate, Issue as IssueSchema
from app.Persistance.session import get_session, UnitOfWork
from app.Configuration.configuration import logger
from typing import List
from app.Core.Domain.Models.issue import Issue
from app.Core.Domain.Models.user import User
from app.Core.Domain.Enums.status import Status
from app.Core.Domain.Enums.severity import Severity
from datetime import datetime

from app.Security.auth_middleware import get_current_user
router = APIRouter()

# READ
@router.get("/issues/", response_model=List[IssueSchema])
async def get_all(uow: UnitOfWork = Depends(get_session), user=Depends(get_current_user)):
    try:
        issues: List[Issue] = await uow.issue_repository.get_all()
        if issues is None:
            raise HTTPException(status_code=404, detail="No issues found")
        return issues
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while retrieving issues | {exception}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/issues/{issue_id}", response_model=IssueSchema)
async def get(issue_id: int, uow: UnitOfWork = Depends(get_session), user=Depends(get_current_user)):
    try:
        issue_fdb: Issue = await uow.issue_repository.get_by_id(int(issue_id))
        if issue_fdb is None:
            raise HTTPException(status_code=404, detail="Issue not found")
        return issue_fdb
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while editing issue with id {issue_id} | {exception}")

# CREATE
@router.post("/issues/", response_model=IssueSchema)
async def create(issue: IssueCreate, user=Depends(get_current_user), uow: UnitOfWork = Depends(get_session)):
    try:
        project = await uow.project_repository.get_by_id(issue.project_id)
        if project is None:
            raise HTTPException(404,"Project not found!")
        new_issue = Issue(
            title=issue.title,
            description=issue.description,
            status=Status.NEW,
            severity=issue.severity,
            issue_type=issue.issue_type,
            date_reported=datetime.now(),
            reporter=user
        )
        await uow.add(new_issue)
        await uow.commit()
        return new_issue
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while creating issue | {exception}")
        raise HTTPException(status_code=500, detail="Internal server error")

# UPDATE
@router.put("/issues/{issue_id}", response_model=IssueSchema)
async def edit(issue_id: str, issue: IssueUpdate,  user=Depends(get_current_user), uow: UnitOfWork = Depends(get_session)):
    try:
        issue_fdb: Issue = await uow.issue_repository.get_by_id(int(issue_id))
        if issue_fdb is None:
            raise HTTPException(status_code=404, detail="Issue not found")
        else:
            await issue_fdb.update(issue)
            await uow.mark_dirty(issue_fdb)
            await uow.commit()
            return issue_fdb
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while editing issue with id {issue_id} | {exception}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/issues/{issue_id}")
async def delete(issue_id: str, user=Depends(get_current_user), uow: UnitOfWork = Depends(get_session)):
    try:
        issue = await uow.issue_repository.get_by_id(int(issue_id))
        if issue is None:
            raise HTTPException(status_code=404, detail="Issue not found")
        else:
            await uow.mark_deleted(issue)
            await uow.commit()
            return {"message": "Issue deleted successfully"}
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while deleting issue with id {issue_id} | {exception}")
        raise HTTPException(status_code=500, detail="Internal server error")
