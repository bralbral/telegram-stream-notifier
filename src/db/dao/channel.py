from collections.abc import Sequence

from .base import BaseDAO
from src.db.models import ChannelModel


class ChannelDAO(BaseDAO[ChannelModel]):
    def __init__(self):
        super().__init__(ChannelModel)

    async def get_many(self, *args, **kwargs) -> Sequence[ChannelModel]:
        return (
            await self.model.filter(*args, **kwargs)
            .prefetch_related("user", "type")
            .order_by("-id")
        )

    async def get_first(self, *args, **kwargs) -> ChannelModel | None:
        return (
            await self.model.filter(*args, **kwargs)
            .prefetch_related("user", "type")
            .first()
        )

    async def create(self, obj: ChannelModel) -> ChannelModel | None:
        return await super().create(obj)

    async def get_or_create(self, **kwargs) -> tuple[ChannelModel, bool]:
        return await super().get_or_create(**kwargs)

    async def update(self, obj: ChannelModel) -> ChannelModel | None:
        return await super().update(obj)

    async def delete(self, id: int) -> bool:
        return await super().delete(id)


__all__ = ["ChannelDAO"]
