from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import Optional
from typing import Sequence
from typing import Type
from typing import TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel import SQLModel

from src.logger import logger

T = TypeVar("T", bound=SQLModel)


class BaseDAO(ABC, Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        try:
            statement = select(self.model).where(self.model.id == id)
            result = await self.session.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await logger.aerror(f"Error getting {self.model.__name__} by id: {e}")
            return None

    @abstractmethod
    async def get_all(self) -> Sequence[T]:
        try:
            statement = select(self.model)
            results = await self.session.execute(statement)
            return results.scalars().all()
        except SQLAlchemyError as e:
            await logger.aerror(f"Error getting all {self.model.__name__}: {e}")
            return []

    @abstractmethod
    async def create(self, obj: T) -> Optional[T]:
        try:
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            await logger.aerror(f"Error creating {self.model.__name__}: {e}")
            await self.session.rollback()
            return None

    @abstractmethod
    async def update(self, obj: T) -> Optional[T]:
        try:
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            await logger.aerror(f"Error updating {self.model.__name__}: {e}")
            await self.session.rollback()
            return None

    @abstractmethod
    async def delete(self, id: int) -> bool:
        try:
            obj = await self.session.get(self.model, id)
            if obj:
                await self.session.delete(obj)
                await self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            await logger.aerror(f"Error deleting {self.model.__name__}: {e}")
            await self.session.rollback()
            return False


__all__ = ["BaseDAO"]
