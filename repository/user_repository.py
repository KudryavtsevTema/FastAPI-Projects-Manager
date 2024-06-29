from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.session import get_db
from models.users_models import User


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
        query = select(User).where(User.username==username).options(selectinload(User.user_type))
        result = await self.db.execute(query)
        user = result.scalars().first()
        if not user:
            return None
        return user.user_type.name
    
    async def create_user_to_db(self, new_user):
        self.db.add(new_user)
        await self.db.commit()
        return new_user
    
        
async def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)