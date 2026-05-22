from collections.abc import Sequence

from .base import BaseDAO
from src.db.models import UserModel


class UserDAO(BaseDAO[UserModel]):
    def __init__(self):
        super().__init__(UserModel)

    async def get_many(self, *args, **kwargs) -> Sequence[UserModel]:
        return (
            await self.model.filter(*args, **kwargs)
            .prefetch_related("role")
            .order_by("-id")
        )

    async def get_first(self, *args, **kwargs) -> UserModel | None:
        return await self.model.filter(*args, **kwargs).prefetch_related("role").first()

    async def create(self, obj: UserModel) -> UserModel | None:
        return await super().create(obj)

    async def get_or_create(self, **kwargs) -> tuple[UserModel, bool]:
        return await super().get_or_create(**kwargs)

    async def update(self, obj: UserModel) -> UserModel | None:
        return await super().update(obj)

    async def delete(self, id: int) -> bool:
        return await super().delete(id)


__all__ = ["UserDAO"]
