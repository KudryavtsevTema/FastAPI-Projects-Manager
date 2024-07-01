from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.schemas.projects_schemas import CreateProject, ShowProject
from app.schemas.user_projects import UserProjectDB, UserProject
from app.services.auth_service import checking_credentials
from app.services.project_service import ProjectService, get_project_service
from app.services.user_projects import UserProjectService, get_user_project_service
from app.services.user_rights_service import checking_admin


main_project_router = APIRouter()


@main_project_router.get("/{id}", response_model=ShowProject)
async def get(id: UUID, 
              current_credential = Depends(checking_credentials),
              service: ProjectService = Depends(get_project_service)):
    return await service.show(id)

@main_project_router.post("/", response_model=ShowProject) 
async def create(body: CreateProject, 
                 current_credential = Depends(checking_credentials),
                 project_service: ProjectService = Depends(get_project_service),
                 current_rights = Depends(checking_admin)):
    return await project_service.create_new(body)

@main_project_router.get("/search/", response_model=List[ShowProject])
async def search(project_name: str | None = None,
                         project_start_day: date| None = None,
                         project_end_day: date | None = None,
                         tags: str | None = Query(None),
                         project_service: ProjectService = Depends(get_project_service),
                         current_credential = Depends(checking_credentials)):
    return await project_service.search(project_name, project_start_day, project_end_day, tags)

@main_project_router.post("/join/", response_model=UserProjectDB)
async def join_projects(body: UserProject,
                        current_credential = Depends(checking_credentials),
                        user_project_service: UserProjectService = Depends(get_user_project_service)):
    return await user_project_service.join_project(current_credential, body)
