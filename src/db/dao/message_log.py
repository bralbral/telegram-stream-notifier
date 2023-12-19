from typing import Optional

from sqlalchemy import CursorResult

from ..models import MessageLogORM
from .base import DAO
from .utils import sqlite_async_upsert
from src.dto import MessageLogCreateDTO
from src.dto import MessageLogRetrieveDTO


class MessageLogDAO(DAO):
    async def create(
        self, message_log_schema: MessageLogCreateDTO
    ) -> Optional[MessageLogRetrieveDTO]:
        """
        :param message_log_schema:
        :return:
        """

        result: CursorResult = await sqlite_async_upsert(
            session=self.session,
            model=MessageLogORM,
            data=message_log_schema.model_dump(),
            index_col="message_id",
        )

        message_log_dto: Optional[MessageLogRetrieveDTO]

        if result.lastrowid:
            message_log_dto = await self.get_by_pk(pk=result.lastrowid)
        else:
            message_log_dto = await self.get_by_attr(
                message_id=message_log_schema.message_id
            )

        return message_log_dto


__all__ = ["MessageLogDAO"]
