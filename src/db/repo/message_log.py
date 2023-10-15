from typing import Optional

from sqlalchemy import CursorResult

from ..models import MessageLogOrm
from .base import Repo
from .utils import sqlite_async_upsert
from src.schemas import MessageLogSchema


class MessageLogRepo(Repo):
    async def create(
        self, message_log_schema: MessageLogSchema
    ) -> Optional[MessageLogSchema]:
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

        message_log_dto: Optional[MessageLogSchema]

        if result.lastrowid:
            message_log_dto = await self.get_by_pk(pk=result.lastrowid)
        else:
            message_log_dto = await self.get_by_attr(
                message_id=message_log_schema.message_id
            )

        return message_log_dto


__all__ = ["MessageLogRepo"]
