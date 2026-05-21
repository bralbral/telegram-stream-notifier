from abc import abstractmethod
from typing import Generic
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar

from tortoise.models import Model

from src.logger import logger

T = TypeVar("T", bound=Model)


class BaseDAO(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    @abstractmethod
    async def get_many(self, *args, **kwargs) -> Sequence[T]:
        try:
            return await self.model.filter(*args, **kwargs).order_by("-id")
        except Exception as e:
            await logger.aerror(
                f"Error searching {self.model.__name__} with attributes {kwargs}: {e}"
            )
            return []

    @abstractmethod
    async def get_first(self, *args, **kwargs) -> Optional[T]:
        try:
            return await self.model.filter(*args, **kwargs).first()
        except Exception as e:
            await logger.aerror(
                f"Error searching for one {self.model.__name__} with attributes {kwargs}: {e}"
            )
            return None

    @abstractmethod
    async def create(self, obj: T) -> Optional[T]:
        try:
            await obj.save()
            return obj
        except Exception as e:
            await logger.aerror(f"Error creating {self.model.__name__}: {e}")
            return None

    @abstractmethod
    async def get_or_create(self, **kwargs) -> tuple[T, bool]:
        instance = await self.get_first(**kwargs)
        if instance:
            return instance, False

        instance = self.model(**kwargs)
        obj = await self.create(obj=instance)

        if not obj:
            raise

        return obj, True

    @abstractmethod
    async def update(self, obj: T) -> Optional[T]:
        try:
            await obj.save()
            return obj
        except Exception as e:
            await logger.aerror(f"Error updating {self.model.__name__}: {e}")
            return None

    @abstractmethod
    async def delete(self, id: int) -> bool:
        try:
            obj = await self.model.get_or_none(id=id)
            if obj:
                await obj.delete()
                return True
            return False
        except Exception as e:
            await logger.aerror(f"Error deleting {self.model.__name__}: {e}")
            return False


__all__ = ["BaseDAO"]