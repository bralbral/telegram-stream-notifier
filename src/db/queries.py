from sqlalchemy.ext.asyncio import AsyncSession

from .sqlite_async_upsert import sqlite_async_upsert
from src.db.models import ChannelOrm
from src.db.models import UserOrm
from src.db.schemas import ChannelSchema
from src.db.schemas import UserSchema


async def create_user(session: AsyncSession, user_schema: UserSchema) -> UserOrm:
    user = await sqlite_async_upsert(
        session=session, model=UserOrm, data=user_schema.model_dump(), index_col="id"
    )
    return user


async def create_channel(
    session: AsyncSession, channel_schema: ChannelSchema
) -> ChannelOrm:
    channel = await sqlite_async_upsert(
        session=session, model=UserOrm, data=channel_schema.model_dump(), index_col="id"
    )
    return channel


__all__ = ["create_user"]
