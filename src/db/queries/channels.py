from ..models import ChannelOrm
from ..schemas import ChannelSchema
from .base import Query
from .utils import sqlite_async_upsert


class ChannelQuery(Query):
    async def create(self, channel_schema: ChannelSchema) -> ChannelOrm:
        channel = await sqlite_async_upsert(
            session=self.session,
            model=ChannelOrm,
            data=channel_schema.model_dump(),
            index_col="id",
        )
        return channel


__all__ = ["ChannelQuery"]
