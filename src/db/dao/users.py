from typing import Optional

from sqlalchemy import CursorResult

from ..models import UserOrm
from .base import DAO
from .utils import sqlite_async_upsert
from src.dto import UserCreateDTO


class UserRepo(DAO):
    async def create(self, user_schema: UserCreateDTO) -> Optional[UserCreateDTO]:
        """
        :param user_schema:
        :return:
        """
        result: CursorResult = await sqlite_async_upsert(
            session=self.session,
            model=UserOrm,
            data=user_schema.model_dump(),
            index_col="user_id",
        )

        user_dto: Optional[UserCreateDTO]

        if result.lastrowid:
            user_dto = await self.get_by_pk(pk=result.lastrowid)
        else:
            user_dto = await self.get_by_attr(user_id=user_schema.user_id)

        return user_dto


__all__ = ["UserRepo"]
