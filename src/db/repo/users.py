from ..models import UserOrm
from .base import Repo
from .utils import sqlite_async_upsert
from src.schemas import UserSchema


class UserRepo(Repo):
    async def create(self, user_schema: UserSchema) -> UserOrm:
        user = await sqlite_async_upsert(
            session=self.session,
            model=UserOrm,
            data=user_schema.model_dump(),
            index_col="id",
        )
        return user


__all__ = ["UserRepo"]
