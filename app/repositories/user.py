from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.db.session import get_db
from app.models.users import Users, UserTypes, UsersDetails


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_common(self, username):
        query = select(Users).where(Users.username == username)
        result = await self.db.execute(query)
        if not result:
            return None
        return result.scalar()
    
    async def get_full(self, username):
        query = select(Users).options(joinedload(Users.details)).where(Users.username==username)
        result = await self.db.execute(query)
        if not result:
            return None
        return result.scalar()
    
    async def get_user_type_from_db(self, username):
        query = select(Users).where(Users.username==username)
        result = await self.db.execute(query)
        user = result.scalar()
        if not user:
            return None
        return UserTypes(user.type_id).name
    
    async def create_user_to_db(self, new_user):
        self.db.add(new_user)
        await self.db.commit()
        return None
    
    async def update_to_superuser(self, username):
        try:
            query = (
                update(Users)
                .where(Users.username==username, Users.type_id!=UserTypes.superuser.value)
                .values(type_id=UserTypes.superuser.value)
            )
            result = await self.db.execute(query)
            await self.db.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.db.rollback()
            return False
        
async def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)