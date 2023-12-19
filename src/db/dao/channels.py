from typing import Optional

from sqlalchemy import CursorResult

from ..models import ChannelORM
from .base import DAO
from .utils import sqlite_async_upsert
from src.dto import ChannelCreateDTO
from src.dto import ChannelRetrieveDTO


class ChannelDAO(DAO):
    async def create(
        self, channel_schema: ChannelCreateDTO
    ) -> Optional[ChannelRetrieveDTO]:
        result: CursorResult = await sqlite_async_upsert(
            session=self.session,
            model=ChannelORM,
            data=channel_schema.model_dump(),
            index_col="url",
        )

        channel_dto: Optional[ChannelRetrieveDTO]

        if result.lastrowid:
            channel_dto = await self.get_by_pk(pk=result.lastrowid)
        else:
            channel_dto = await self.get_by_attr(url=channel_schema.url)

        return channel_dto


__all__ = ["ChannelDAO"]
