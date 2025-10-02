from fastapi import FastAPI, Header, HTTPException, APIRouter, Depends
from app.Core.Schemas.project import ProjectCreate, ProjectUpdate, Project as ProjectSchema
from app.Persistance.session import get_session, UnitOfWork
from app.Configuration.configuration import logger
from typing import List
from app.Core.Domain.Models.project import Project
from app.Security.auth_middleware import get_current_user

router = APIRouter()
    

# READ
@router.get("/projects/", response_model=List[ProjectSchema])
async def get_projects(uow: UnitOfWork = Depends(get_session), user=Depends(get_current_user)):
    try:
        project_fdb: List[Project] = await uow.project_repository.get_all(user)
        if project_fdb is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return project_fdb
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while retrieving projects | {exception}")


@router.get("/projects/{project_id}", response_model=ProjectSchema)
async def get(project_id: str, uow: UnitOfWork = Depends(get_session), user=Depends(get_current_user)):
    try:
        project_fdb: Project = await uow.project_repository.get_by_id(project_id, user)
        if project_fdb is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return project_fdb
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while editing project with id {project_id} | {exception}")

# CREATE
@router.post("/projects/")
async def create(project: ProjectCreate, uow: UnitOfWork = Depends(get_session), user=Depends(get_current_user)):
    try:
        new_project = Project(
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            end_date=project.end_date,
            users=[user]
        )
        await uow.add(new_project)
        await uow.commit()
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while creating project | {exception}")


# UPDATE
@router.put("/projects/{project_id}")
async def edit(project_id: str, project: ProjectUpdate, user=Depends(get_current_user), uow: UnitOfWork = Depends(get_session)):
    try:
        project_fdb: Project = await uow.project_repository.get_by_id(int(project_id), user)
        
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        else:
            await project_fdb.update(project,[user])
            await uow.mark_dirty(project_fdb)
            await uow.commit()
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while editing project with id {project_id} | {exception}")

# DELETE


@router.delete("/projects/{project_id}")
async def delete_project(project_id: str, user=Depends(get_current_user), uow: UnitOfWork = Depends(get_session)):
    try:
        project = await uow.project_repository.get_by_id(int(project_id), user
                                                         )
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        else:
            await uow.mark_deleted(project)
            await uow.commit()
    except Exception as exception:
        logger.error(
            f"[Exception] : Exception occured while deleting project with id {project_id} | {exception}")
