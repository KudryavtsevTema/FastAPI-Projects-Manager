from datetime import date
from uuid import UUID
from schemas.projects_schemas import CreateProject
from services.auth_service import checking_credentials
from services.project_service import ProjectService, get_project_service
from fastapi import APIRouter, Depends, Query

from services.user_rights_service import checking_admin


main_project_router = APIRouter()


@main_project_router.get("/{id}")
async def get(id: UUID, 
              current_credential = Depends(checking_credentials),
              service: ProjectService = Depends(get_project_service)):
    return await service.show(id)

@main_project_router.post("/") 
async def create(body: CreateProject, 
                 current_credential = Depends(checking_credentials),
                 project_service: ProjectService = Depends(get_project_service),
                 current_rights = Depends(checking_admin)):
    return await project_service.create_new(body)

@main_project_router.get("/search/")
async def search(project_name: str | None = None,
                         project_start_day: date| None = None,
                         project_end_day: date | None = None,
                         tags: str | None = Query(None),
                         project_service: ProjectService = Depends(get_project_service),
                         current_credential = Depends(checking_credentials)):
    return await project_service.search(project_name, project_start_day, project_end_day, tags)
