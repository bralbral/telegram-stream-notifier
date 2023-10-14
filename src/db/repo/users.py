from typing import Optional

from pydantic import TypeAdapter
from sqlalchemy import CursorResult
from sqlalchemy import ScalarResult
from sqlalchemy import Select
from sqlalchemy import true

from ..exceptions import ColumnDoesNotExist
from ..models import UserOrm
from .base import Repo
from .utils import sqlite_async_upsert
from src.schemas import UserSchema


class UserRepo(Repo):
    async def create(self, user_schema: UserSchema) -> Optional[UserSchema]:
        result: CursorResult = await sqlite_async_upsert(
            session=self.session,
            model=UserOrm,
            data=user_schema.model_dump(),
            index_col="user_id",
        )

        user_dto: Optional[UserSchema]

        if result.lastrowid:
            user_dto = await self.get_by_pk(pk=result.lastrowid)
        else:
            user_dto = await self.get_by_attr(user_id=user_schema.user_id)

        return user_dto

    async def get_by_attr(self, **kwargs) -> Optional[UserSchema]:
        where_clause: list = []

        for key in kwargs.keys():
            if not hasattr(UserOrm, key):
                raise ColumnDoesNotExist(column=key, table=UserOrm.__tablename__)
            else:
                col = getattr(UserOrm, key)
                where_clause.append(col == kwargs[key])

        stm = Select(UserOrm).where(*where_clause)

        result: ScalarResult = await self.session.scalars(stm)
        user: Optional[UserOrm] = result.first()

        if user:
            user_dto = UserSchema.model_validate(user)
            return user_dto

        return None

    async def get_by_pk(self, pk: int) -> Optional[UserSchema]:
        stm = Select(UserOrm).where(UserOrm.id == pk)

        result: ScalarResult = await self.session.scalars(stm)
        user: Optional[UserOrm] = result.first()

        if user:
            user_dto = UserSchema.model_validate(user)
            return user_dto

        return None

    async def get_superusers(self) -> list[UserSchema]:
        stm = Select(UserOrm).where(UserOrm.is_superuser == true()).order_by(UserOrm.id)

        result = await self.session.scalars(stm)

        ta = TypeAdapter(list[UserSchema])
        users = ta.validate_python(result.all())

        return users


__all__ = ["UserRepo"]
