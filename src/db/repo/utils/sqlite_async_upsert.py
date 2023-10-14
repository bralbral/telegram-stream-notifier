import copy
from typing import Any
from typing import Type

from sqlalchemy import CursorResult
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession


# source
# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#insert-on-conflict-upsert


async def sqlite_async_upsert(
    session: AsyncSession,
    model: Type[Any],
    data: dict[str, Any],
    index_col: str,
    pk_col: str = "id",
) -> CursorResult:
    """
    :param pk_col:
    :param session:
    :param model:
    :param data:
    :param index_col:
    :return:
    """

    data_without_index = copy.deepcopy(data)

    if index_col in data_without_index.keys():
        data_without_index.pop(index_col)

    if pk_col in data_without_index.keys():
        data_without_index.pop(pk_col)

    insert_stmt = insert(model).values(**data)
    do_update_stmt = insert_stmt.on_conflict_do_update(
        index_elements=[index_col], set_=data_without_index
    )

    result = await session.execute(do_update_stmt)
    await session.commit()

    return result


__all__ = ["sqlite_async_upsert"]
