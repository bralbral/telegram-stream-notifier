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

    @property
    def __prepare_select_statement(self):
        statement = (
            select(self.model)
            .options(joinedload(self.model.user_role))
            .options(joinedload(self.model.channel_type))
        )
        return statement

    async def get_many(self, **kwargs) -> Sequence[ChannelModel]:
        try:
            statement = self.__prepare_select_statement.filter_by(**kwargs)
            results = await self.session.execute(statement)
            return results.scalars().all()
        except SQLAlchemyError as e:
            await logger.aerror(
                f"Error searching {self.model.__name__} with attributes {kwargs}: {e}"
            )
            return []

    async def get_first(self, **kwargs) -> Optional[ChannelModel]:
        try:
            statement = self.__prepare_select_statement.filter_by(**kwargs)
            result = await self.session.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await logger.aerror(
                f"Error searching for one {self.model.__name__} with attributes {kwargs}: {e}"
            )
            return None

    async def create(self, obj: ChannelModel) -> Optional[ChannelModel]:
        return await super().create(obj)

    async def update(self, obj: ChannelModel) -> Optional[ChannelModel]:
        return await super().update(obj)

    async def delete(self, id: int) -> bool:
        return await super().delete(id)


__all__ = ["ChannelDAO"]
