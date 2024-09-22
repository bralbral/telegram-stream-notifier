from typing import Optional
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .base import BaseDAO
from src.db.models import MessageLogModel


class MessageLogDAO(BaseDAO[MessageLogModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MessageLogModel)

    @property
    def __prepare_select_statement(self):
        statement = select(self.model).order_by(self.model.id)
        return statement

    async def get_first(self, **kwargs) -> Optional[MessageLogModel]:
        return await super().get_first(**kwargs)

    async def get_many(self, **kwargs) -> Sequence[MessageLogModel]:
        return await super().get_many(**kwargs)

    async def create(self, obj: MessageLogModel) -> Optional[MessageLogModel]:
        return await super().create(obj)

    async def update(self, obj: MessageLogModel) -> Optional[MessageLogModel]:
        return await super().update(obj)

    async def delete(self, id: int) -> bool:
        return await super().delete(id)


__all__ = ["MessageLogDAO"]
