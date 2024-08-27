from typing import Optional

from sqlalchemy import CursorResult

from ..models import UserORM
from .base import DAO
from .utils import sqlite_async_upsert
from src.dto import UserCreateDTO
from src.dto import UserRetrieveDTO


class UserDAO(DAO):
    async def create(self, user_schema: UserCreateDTO) -> Optional[UserRetrieveDTO]:
        """
        :param user_schema:
        :return:
        """
        result: CursorResult = await sqlite_async_upsert(
            session=self.session,
            model=UserORM,
            data=user_schema.model_dump(),
            index_col="user_id",
        )

        user_dto: Optional[UserRetrieveDTO]

        if result.lastrowid:
            user_dto = await self.get_by_pk(pk=result.lastrowid)
        else:
            user_dto = await self.get_by_attr(user_id=user_schema.user_id)

        return user_dto


__all__ = ["UserDAO"]
