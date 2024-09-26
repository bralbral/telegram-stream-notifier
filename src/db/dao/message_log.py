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

    async def get_first(self, *args, **kwargs) -> Optional[MessageLogModel]:
        return await super().get_first(*args, **kwargs)

    async def get_many(self, *args, **kwargs) -> Sequence[MessageLogModel]:
        return await super().get_many(*args, **kwargs)

    async def create(self, obj: MessageLogModel) -> Optional[MessageLogModel]:
        return await super().create(obj)

    async def get_or_create(self, **kwargs) -> tuple[MessageLogModel, bool]:
        return await super().get_or_create(**kwargs)

    async def update(self, obj: MessageLogModel) -> Optional[MessageLogModel]:
        return await super().update(obj)

    async def delete(self, id: int) -> bool:
        return await super().delete(id)


__all__ = ["MessageLogDAO"]
