from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from src.constants import SQLITE_DATABASE_FILE_PATH

engine = create_async_engine(
    f"sqlite+aiosqlite:///{SQLITE_DATABASE_FILE_PATH}", future=True
)

session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=True
)


__all__ = ["engine", "session_maker"]
