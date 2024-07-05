from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from sqlalchemy.orm import joinedload

from app.models.projects import Projects, ProjectsDetails, StatusType
from app.db.session import get_db

class ProjectsRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_common(self, id):
        query = select(Projects).where(Projects.id==id)
        project = await self.db.execute(query)
        if not project:
            return None
        return project.scalar()
    
    async def get_full(self, id):
        query = select(Projects).options(joinedload(Projects.details)).where(Projects.id==id)
        project = await self.db.execute(query)
        if not project:
            return None
        return project.scalar()

    async def create_to_db(self, project: Projects): 
        self.db.add(project)
        await self.db.commit()
        return project

    async def search_from_db(self, name=None, start_at=None, end_at=None, tags: list=None):
        query = (
            select(Projects)
            .join(ProjectsDetails, Projects.id == ProjectsDetails.project_id)
            .options(joinedload(Projects.details))
        )

        if name is not None:
            query = query.where(Projects.name == name)

        if start_at is not None:
            query = query.where(ProjectsDetails.start_at > start_at)
        
        if end_at is not None:
            query = query.where(ProjectsDetails.end_at < end_at)
    
        if tags is not None:
            for tag in tags:
                query = query.filter(ProjectsDetails.tags.contains([tag]))
            
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def set_remaining_investment(self, project_id, remaining_investment):
        query=update(ProjectsDetails).where(ProjectsDetails.project_id==project_id).values(remaining_required_investment=remaining_investment)
        await self.db.execute(query)
        await self.db.commit()
    
    async def delete(self, id):
        query = update(Projects).where(Projects.id==id).values(status=StatusType.deleted.value)
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_common(id)
    
    async def get_status(self, id):
        query = select(Projects.status).where(Projects.id==id)
        status = await self.db.execute(query)
        return status.scalar()
    
async def get_project_repository(db: AsyncSession = Depends(get_db)):
    return ProjectsRepository(db)