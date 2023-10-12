from ..models import UserOrm
from ..schemas import UserSchema
from .base import Query
from .utils import sqlite_async_upsert


class UserQuery(Query):
    async def create(self, user_schema: UserSchema) -> UserOrm:
        user = await sqlite_async_upsert(
            session=self.session,
            model=UserOrm,
            data=user_schema.model_dump(),
            index_col="id",
        )
        return user


__all__ = ["UserQuery"]
