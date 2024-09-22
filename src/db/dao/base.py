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


class BaseDAO(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    @property
    def __prepare_select_statement(self):
        statement = select(self.model)
        return statement

    @abstractmethod
    async def get_many(self, **kwargs) -> Sequence[T]:
        try:
            statement = self.__prepare_select_statement.filter_by(**kwargs)
            results = await self.session.execute(statement)
            return results.scalars().all()
        except SQLAlchemyError as e:
            await logger.aerror(
                f"Error searching {self.model.__name__} with attributes {kwargs}: {e}"
            )
            return []

    @abstractmethod
    async def get_first(self, **kwargs) -> Optional[T]:
        try:
            statement = self.__prepare_select_statement.filter_by(**kwargs)
            result = await self.session.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as e:
            await logger.aerror(
                f"Error searching for one {self.model.__name__} with attributes {kwargs}: {e}"
            )
            return None

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
