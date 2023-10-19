from typing import Optional

from sqlalchemy import CursorResult

from ..models import ChannelOrm
from .base import Repo
from .utils import sqlite_async_upsert
from src.schemas import ChannelSchema


class ChannelRepo(Repo):
    async def create(self, channel_schema: ChannelSchema) -> Optional[ChannelSchema]:
        result: CursorResult = await sqlite_async_upsert(
            session=self.session,
            model=ChannelOrm,
            data=channel_schema.model_dump(),
            index_col="url",
        )

        channel_dto: Optional[ChannelSchema]

        if result.lastrowid:
            channel_dto = await self.get_by_pk(pk=result.lastrowid)
        else:
            channel_dto = await self.get_by_attr(url=channel_schema.url)

        return channel_dto


__all__ = ["ChannelRepo"]
