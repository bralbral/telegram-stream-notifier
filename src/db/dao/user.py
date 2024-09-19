from typing import Optional
from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from .base import BaseDAO
from src.db.models import UserModel
from src.logger import logger


class UserDAO(BaseDAO[UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    async def get_by_id(self, id: int) -> Optional[UserModel]:
        try:
            statement = (
                select(self.model)
                .where(self.model.id == id)
                .options(joinedload(self.model.user_role))
            )
            result = await self.session.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await logger.aerror(
                f"Error getting {self.model.__name__} by id with relationships: {e}"
            )
            return None

    async def get_all(self) -> Sequence[UserModel]:
        try:
            statement = select(self.model).options(joinedload(self.model.user_role))
            results = await self.session.execute(statement)
            return results.scalars().all()
        except SQLAlchemyError as e:
            await logger.aerror(
                f"Error getting all {self.model.__name__} with relationships: {e}"
            )
            return []

    async def create(self, obj: UserModel) -> Optional[UserModel]:
        return await super().create(obj)

    async def update(self, obj: UserModel) -> Optional[UserModel]:
        return await super().update(obj)

    async def delete(self, id: int) -> bool:
        return await super().delete(id)


__all__ = ["UserDAO"]
