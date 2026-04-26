import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

#DATABASE_URL = "postgresql+asyncpg://events_user:1234@localhost:5432/events_db"

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_STRING")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
