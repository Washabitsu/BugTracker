from fastapi import FastAPI, Header, HTTPException, APIRouter, Depends
from app.Api.authorization import get_current_user, get_admin, get_developer
from app.Core.Schemas.project import ProjectCreate, ProjectUpdate, Project as ProjectSchema
from app.Persistance.session import get_session, UnitOfWork
from app.Configuration.configuration import logger
from typing import List
from app.Core.Domain.Models.project import Project
router = APIRouter()


# READ
@router.get("/projects/", response_model=List[ProjectSchema])
async def get_projects(uow: UnitOfWork = Depends(get_session)):
    try:
        project_fdb: List[Project] = await uow.project_repository.get_all()
        if project_fdb is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return project_fdb
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while retrieving projects | {exception}")


@router.get("/projects/{project_id}", response_model=ProjectSchema)
async def get(project_id: int, uow: UnitOfWork = Depends(get_session)):
    try:
        project_fdb: Project = await uow.project_repository.get_by_id(int(project_id))
        if project_fdb is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return project_fdb
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while editing project with id {project_id} | {exception}")

# CREATE
@router.post("/projects/")
async def create(project: ProjectCreate, username=Depends(get_admin), uow: UnitOfWork = Depends(get_session)):
    try:
        users = await uow.user_repository.get_by_ids(project.users_ids)
        new_project = Project(
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            end_date=project.end_date,
            users=users
        )
        await uow.add(new_project)
        await uow.commit()
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while creating project | {exception}")


# UPDATE
@router.put("/projects/{project_id}")
async def edit(project_id: str, project: ProjectUpdate, username=Depends(get_admin), uow: UnitOfWork = Depends(get_session)):
    try:
        project_fdb: Project = await uow.project_repository.get_by_id(int(project_id))
        users = await uow.user_repository.get_by_ids(project.users_ids)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        else:
            await project_fdb.update(project,users)
            await uow.mark_dirty(project_fdb)
            await uow.commit()
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while editing project with id {project_id} | {exception}")

# DELETE


@router.delete("/projects/{project_id}")
async def delete_project(project_id: str, username=Depends(get_admin), uow: UnitOfWork = Depends(get_session)):
    try:
        project = await uow.project_repository.get_by_id(int(project_id))
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        else:
            await uow.mark_deleted(project)
            await uow.commit()
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while deleting project with id {project_id} | {exception}")
