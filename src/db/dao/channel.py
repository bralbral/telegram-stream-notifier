from typing import Optional
from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from .base import BaseDAO
from src.db.models import ChannelModel
from src.logger import logger


class ChannelDAO(BaseDAO[ChannelModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChannelModel)

    async def get_by_id(self, id: int) -> Optional[ChannelModel]:
        try:
            statement = (
                select(self.model)
                .where(self.model.id == id)
                .options(joinedload(self.model.channel_type))
            )
            result = await self.session.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await logger.aerror(
                f"Error getting {self.model.__name__} by id with relationships: {e}"
            )
            return None

    async def get_all(self) -> Sequence[ChannelModel]:
        try:
            statement = select(self.model).options(joinedload(self.model.channel_type))
            results = await self.session.execute(statement)
            return results.scalars().all()
        except SQLAlchemyError as e:
            await logger.aerror(
                f"Error getting all {self.model.__name__} with relationships: {e}"
            )
            return []

    async def create(self, obj: ChannelModel) -> Optional[ChannelModel]:
        return await super().create(obj)

    async def update(self, obj: ChannelModel) -> Optional[ChannelModel]:
        return await super().update(obj)

    async def delete(self, id: int) -> bool:
        return await super().delete(id)


__all__ = ["ChannelDAO"]
