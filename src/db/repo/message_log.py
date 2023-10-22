from typing import Optional

from sqlalchemy import CursorResult

from ..models import MessageLogOrm
from .base import Repo
from .utils import sqlite_async_upsert
from src.dto import MessageLogDTO


class MessageLogRepo(Repo):
    async def create(
        self, message_log_schema: MessageLogDTO
    ) -> Optional[MessageLogDTO]:
        """
        :param message_log_schema:
        :return:
        """

        result: CursorResult = await sqlite_async_upsert(
            session=self.session,
            model=MessageLogOrm,
            data=message_log_schema.model_dump(),
            index_col="message_id",
        )

        message_log_dto: Optional[MessageLogDTO]

        if result.lastrowid:
            message_log_dto = await self.get_by_pk(pk=result.lastrowid)
        else:
            message_log_dto = await self.get_by_attr(
                message_id=message_log_schema.message_id
            )

        return message_log_dto


__all__ = ["MessageLogRepo"]
