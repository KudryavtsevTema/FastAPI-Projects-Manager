from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.users_models import User, UserTypes


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_from_db(self, username) -> User:
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        if not result:
            return None
        return result.scalars().first()
    
    async def get_user_type_from_db(self, username):
        query = select(User).where(User.username==username)
        result = await self.db.execute(query)
        user = result.scalars().first()
        if not user:
            return None
        return UserTypes(user.type_id).name
    
    async def create_user_to_db(self, new_user):
        self.db.add(new_user)
        await self.db.commit()
        return new_user
    
        
async def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)