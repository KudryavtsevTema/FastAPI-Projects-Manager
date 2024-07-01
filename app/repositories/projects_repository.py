from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends

from app.models.projects_models import Project
from app.db.session import get_db

class ProjectsRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_from_db(self, id):
        project = await self.db.get(Project, id) 
        if not project:
            return None
        return project


    async def create_to_db(self, new_project: Project): 
        self.db.add(new_project)
        await self.db.commit()
        return new_project

    async def search_from_db(self, name, start_at, end_at, tags: list):
        query = select(Project)

        if name is not None:
            query = query.where(Project.name == name)

        if start_at is not None:
            query = query.where(Project.start_at > start_at)
        
        if end_at is not None:
            query = query.where(Project.end_at < end_at)
    
        if tags is not None:
            for tag in tags:
                query = query.filter(Project.tags.contains([tag]))
            
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def set_remaining_investment(self, project_id, remaining_investment):
        query=update(Project).where(Project.id==project_id).values(remaining_required_investment=remaining_investment)
        await self.db.execute(query)
        await self.db.commit()

async def get_project_repository(db: AsyncSession = Depends(get_db)):
    return ProjectsRepository(db)