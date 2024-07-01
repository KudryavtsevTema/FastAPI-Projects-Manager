from http import HTTPStatus
from datetime import datetime

from fastapi import HTTPException, Depends


from app.models.users_projects import UserProjects
from app.repositories.user_repository import UserRepository, get_user_repository
from app.repositories.projects_repository import ProjectsRepository, get_project_repository
from app.repositories.user_project_repository import UserProjectRepository, get_user_project_repository
from app.schemas.user_projects import UserProject, UserProjectDB

class UserProjectService:
    def __init__(self, 
                 user_repository: UserRepository,
                 project_repository: ProjectsRepository,
                 user_project_repository: UserProjectRepository):
        self.user_repository = user_repository
        self.project_repository = project_repository
        self.user_project_repository = user_project_repository

    async def join_project(self, decoded_jwt, data: UserProject):
        username = decoded_jwt.get('username')
        user = await self.user_repository.get_user_from_db(username)
        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"User {username} not exists")
        project = await self.project_repository.get_from_db(data.project_id)
        if not project:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Project {data.project_id} not found")
        if data.investment_sum > project.remaining_required_investment:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, 
                detail=f"""
                    Investment sum {data.investment_sum} couldn't be greater than 
                    requirements investment {project.remaining_required_investment}
                """)
        user_project = UserProjectDB(
            project_id=project.id,
            investment_sum=data.investment_sum,
            user_id=user.id,
            join_datetime=datetime.now())
        user_project_model = UserProjects(**user_project.model_dump())
        await self.user_project_repository.create_user_project(user_project_model)
        await self.project_repository.set_remaining_investment(
            project.id,
            project.remaining_required_investment-data.investment_sum)
        return user_project

async def get_user_project_service(
        project_repository: ProjectsRepository = Depends(get_project_repository), 
        user_repository: UserRepository = Depends(get_user_repository),
        user_project_repository: UserProjectRepository = Depends(get_user_project_repository)
        ):
    return UserProjectService(user_repository, project_repository, user_project_repository)