from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from .db_session import DbSessionMiddleware


def setup_middlewares(
    dp: Dispatcher, session_maker: async_sessionmaker[AsyncSession]
) -> None:
    dp.message.outer_middleware(DbSessionMiddleware(session_pool=session_maker))


__all__ = ["setup_middlewares"]
