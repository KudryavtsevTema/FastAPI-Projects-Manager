from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from settings import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with async_session() as session:  # Правильное создание сессии
        try:
            yield session
        finally:
            await session.close()