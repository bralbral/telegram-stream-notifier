from abc import ABC
from typing import Any
from typing import Optional
from typing import Type

from pydantic import TypeAdapter
from sqlalchemy import Delete
from sqlalchemy import inspect
from sqlalchemy import ScalarResult
from sqlalchemy import Select
from sqlalchemy import Update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.exceptions import ColumnDoesNotExist
from src.db.models import ModelORM
from src.dto import DTO


class DAO(ABC):
    def __init__(
        self, session: AsyncSession, model_orm: Type[ModelORM], schema: Type[DTO]
    ) -> None:
        self.session = session
        self.model_orm = model_orm
        self.schema = schema

    @property
    def relations(self):
        """
        Get all relations
        :return:
        """
        return {
            tuple_name_column[0]: tuple_name_column[1]
            for tuple_name_column in inspect(self.model_orm).relationships.items()
        }

    async def scalars(self, statement):
        """
        :param statement: sqlalchemy statement, for example sqlalchemy.select
        :return:
        """
        for relation in self.relations.values():
            statement = statement.options(selectinload(relation))

        return await self.session.scalars(statement)

    async def create(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    def __generate_predicate(self, **kwargs) -> list:
        where_clause: list = []

        for key in kwargs.keys():
            if not hasattr(self.model_orm, key):
                raise ColumnDoesNotExist(column=key, table=self.model_orm.__tablename__)
            else:
                col = getattr(self.model_orm, key)
                where_clause.append(col == kwargs[key])

        return where_clause

    async def __get_by_attrs(self, **kwargs) -> ScalarResult:
        """
        :param kwargs:
        :return:
        """
        stm = (
            Select(self.model_orm)
            .where(*self.__generate_predicate(**kwargs))
            .order_by(self.model_orm.id.desc())
        )
        result: ScalarResult = await self.scalars(statement=stm)
        return result

    async def list_by_attrs(self, **kwargs) -> list[DTO]:
        """
        :param kwargs:
        :return:
        """
        result: ScalarResult = await self.__get_by_attrs(**kwargs)
        all_results = result.all()
        ta = TypeAdapter(list[self.schema])  # type: ignore
        dto_objects = ta.validate_python(all_results)

        return dto_objects

    async def get_by_pk(self, pk: int) -> Optional[DTO]:
        """
        :param pk:
        :return:
        """
        stm = Select(self.model_orm).where(self.model_orm.id == pk)

        result: ScalarResult = await self.scalars(statement=stm)
        model: Optional[ModelORM] = result.first()

        if model:
            dto = self.schema.model_validate(model)
            return dto

        return None

    async def get_by_attr(self, **kwargs) -> Optional[DTO]:
        """
        :param kwargs:
        :return:
        """
        result: ScalarResult = await self.__get_by_attrs(**kwargs)
        model: Optional[ModelORM] = result.first()

        if model:
            dto = self.schema.model_validate(model)
            return dto

        return None

    async def delete_by_pk(self, pk: int) -> Optional[int]:
        stm = (
            Delete(self.model_orm)
            .where(self.model_orm.id == pk)
            .returning(self.model_orm.id)
        )
        result: ScalarResult = await self.session.scalars(statement=stm)
        deleted_id = result.first()

        await self.session.commit()
        return deleted_id

    async def delete_by_attr(self, **kwargs) -> list[int]:
        """
        :param kwargs:
        :return:
        """
        stm = (
            Delete(self.model_orm)
            .where(*self.__generate_predicate(**kwargs))
            .returning(self.model_orm.id)
        )

        result: ScalarResult = await self.session.scalars(statement=stm)

        await self.session.commit()
        return list(result.all())

    async def update_by_pk(self, pk: int, data: dict) -> Optional[int]:
        stm = (
            Update(self.model_orm)
            .where(self.model_orm.id == pk)
            .values(**data)
            .returning(self.model_orm.id)
        )
        result: ScalarResult = await self.session.scalars(statement=stm)
        updated_id = result.first()

        await self.session.commit()
        return updated_id


__all__ = ["DAO"]
