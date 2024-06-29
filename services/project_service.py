from fastapi import Depends

from schemas.projects_schemas import CreateProject
from repository.projects_repository import ProjectsRepository, get_project_repository
from models.projects_models import Project


class ProjectService:
    def __init__(self, repository: ProjectsRepository):
        self.repository = repository

    async def show(self, id):
        return await self.repository.get_from_db(id)

    async def create_new(self, project: CreateProject):
        model = Project(**project.model_dump())
        return await self.repository.create_to_db(model)

    async def search(self, name, start_day, end_day, tags):
        tags_list = tags.split(",")
        tags_list = [tag.strip() for tag in tags_list]
        return await self.repository.search_from_db(name, start_day, end_day, tags_list)
    
async def get_project_service(repository: ProjectsRepository = Depends(get_project_repository)):
    return ProjectService(repository)