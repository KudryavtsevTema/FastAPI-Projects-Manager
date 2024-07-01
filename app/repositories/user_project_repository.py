from sqlalchemy import Update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.session import get_db
from app.models.users_projects import UserProjects


class UserProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user_project(self, data: UserProjects):
        self.db.add(data)
        await self.db.commit()
        return data

async def get_user_project_repository(db: AsyncSession = Depends(get_db)):
    return UserProjectRepository(db)