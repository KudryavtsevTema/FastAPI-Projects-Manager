from fastapi import Depends, HTTPException

from app.schemas.projects import BaseResponseProject, BaseProject, DetailedResponseProject
from app.repositories.projects import ProjectsRepository, get_project_repository
from app.models.projects import Projects, ProjectsDetails, StatusType


class ProjectService:
    def __init__(self, project_repository: ProjectsRepository):
        self.project_repository = project_repository

    async def get_common(self, id):
        project =  await self.project_repository.get_common(id)
        if not project or (await self.is_deleted(id)):
            raise HTTPException(status_code=404, detail="Project not found")
        else:
            return await self.create_common_response(project)
    
    async def get_full(self, id):
        project = await self.project_repository.get_full(id)
        if not project or await self.is_deleted(id):
            raise HTTPException(status_code=404, detail="Project not found")
        return await self.create_detailed_response(project)
        
    async def create_new(self, project: BaseProject):
        project_model = Projects(
            name=project.name,
            description=project.description,
            details=ProjectsDetails(
                start_at=project.start_at,
                end_at=project.end_at,
                total_required_investment=project.total_required_investment,
                remaining_required_investment=project.remaining_required_investment,
                min_investment=project.min_investment,
                tags=project.tags
                )
            )
        project_response = await self.project_repository.create_to_db(project_model)   
        return await self.create_common_response(project_response)

    async def search(self, name=None, start_day=None, end_day=None, tags=None):
        if tags is not None:
            tags_list = tags.split(",")
            tags_list = [tag.strip() for tag in tags_list]
            projects = await self.project_repository.search_from_db(name, start_day, end_day, tags_list)
            project_list = list()
            for project in projects:
                if not await self.is_deleted(project.id):
                    detailed_response = await self.create_detailed_response(project)
                    project_list.append(detailed_response)
            return project_list
            
        projects = await self.project_repository.search_from_db(name, start_day, end_day, tags)
        project_list = list()
        for project in projects:
            if not await self.is_deleted(project.id):
                detailed_response = await self.create_detailed_response(project)
                project_list.append(detailed_response)
        return project_list

    async def delete(self, id):
        response_project = await self.project_repository.delete(id)
        return await self.create_common_response(response_project)
    
    async def is_deleted(self, id):
        status = await self.project_repository.get_status(id)
        return StatusType(status).name == "deleted"

    async def create_detailed_response(self, project):
        project_data = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "status": StatusType(project.status).name,
                "start_at": project.details.start_at,
                "end_at": project.details.end_at,
                "total_required_investment": project.details.total_required_investment,
                "remaining_required_investment": project.details.remaining_required_investment,
                "min_investment": project.details.min_investment,
                "tags": project.details.tags
            }
        detailed_response = DetailedResponseProject(**project_data)
        return detailed_response
    
    async def create_common_response(self, project):
        return BaseResponseProject(
            id=project.id,
            name=project.name,
            description=project.description,
            status=StatusType(project.status).name
            )

    
async def get_project_service(project_repository: ProjectsRepository = Depends(get_project_repository)):
    return ProjectService(project_repository)