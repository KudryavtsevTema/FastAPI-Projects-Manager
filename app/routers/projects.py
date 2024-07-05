from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.schemas.projects import DetailedResponseProject, BaseResponseProject, BaseProject
from app.schemas.user_projects import UserProjectDB, BaseUserProject
from app.services.auth import checking_credentials
from app.services.projects import ProjectService, get_project_service
from app.services.user_projects import UserProjectService, get_user_project_service
from app.services.user_rights import checking_admin


main_project_router = APIRouter()


@main_project_router.get("/common/{id}", response_model=BaseResponseProject)
async def read_common_project(id: UUID,
              project_service: ProjectService = Depends(get_project_service)):
    """Endpoint for getting some info about project by UUID"""
    return await project_service.get_common(id)

@main_project_router.get("/full/{id}", response_model=DetailedResponseProject)
async def read_full_project(id: UUID,
              project_service: ProjectService = Depends(get_project_service)):
    """Endpoint for getting all info about project by UUID"""
    return await project_service.get_full(id)

@main_project_router.post("/new", response_model=BaseResponseProject)
async def create(body: BaseProject,
                 project_service: ProjectService = Depends(get_project_service),
                 current_credential = Depends(checking_credentials),
                 is_admin = Depends(checking_admin)):
    """Endpoint for creating a new project"""
    return await project_service.create_new(body)

@main_project_router.get("/search", response_model=List[DetailedResponseProject])
async def search(project_name: str | None = None, 
                 project_start_day: date| None = None,
                 project_end_day: date | None = None,
                 tags: str | None = Query(None),
                 project_service: ProjectService = Depends(get_project_service),
                 current_credential = Depends(checking_credentials)):
    """Endpoint for searching projects by any information"""
    return await project_service.search(project_name, project_start_day, project_end_day, tags)

@main_project_router.post("/join/", response_model=UserProjectDB)
async def join_projects(body: BaseUserProject,
                        current_credential = Depends(checking_credentials),
                        user_project_service: UserProjectService = Depends(get_user_project_service)):
    """Endpoint for joining a project with a payment of any amount(more than min_investment)"""
    return await user_project_service.join_project(current_credential, body)

@main_project_router.patch("/delete", response_model=BaseResponseProject)
async def delete(id:UUID,
                 project_service: ProjectService = Depends(get_project_service),
                 current_credential = Depends(checking_credentials),
                 is_admin = Depends(checking_admin)):
    """Endpoint to delete project by id"""
    return await project_service.delete(id)