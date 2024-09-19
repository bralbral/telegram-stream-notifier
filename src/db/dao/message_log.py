from typing import Optional
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from src.db.models import MessageLogModel


class MessageLogDAO(BaseDAO[MessageLogModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MessageLogModel)

    async def get_by_id(self, id: int) -> Optional[MessageLogModel]:
        return await super().get_by_id(id)

    async def get_all(self) -> Sequence[MessageLogModel]:
        return await super().get_all()

    async def create(self, obj: MessageLogModel) -> Optional[MessageLogModel]:
        return await super().create(obj)

    async def update(self, obj: MessageLogModel) -> Optional[MessageLogModel]:
        return await super().update(obj)

    async def delete(self, id: int) -> bool:
        return await super().delete(id)


__all__ = ["MessageLogDAO"]
