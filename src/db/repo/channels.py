from ..models import ChannelOrm
from .base import Repo
from .utils import sqlite_async_upsert
from src.schemas import ChannelSchema


class ChannelRepo(Repo):
    async def create(self, channel_schema: ChannelSchema) -> ChannelOrm:
        channel = await sqlite_async_upsert(
            session=self.session,
            model=ChannelOrm,
            data=channel_schema.model_dump(),
            index_col="id",
        )
        return channel


__all__ = ["ChannelRepo"]
