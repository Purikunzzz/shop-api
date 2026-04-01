from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)

from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# connect to database
engine = create_async_engine(
    settings.DATABASE_URL,
    echo = settings.DEBUG
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base Class
class Base(DeclarativeBase):
    pass

# Depency - FastAPI will call when it has request
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
