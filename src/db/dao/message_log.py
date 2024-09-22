from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from src.db.models import MessageLogModel


class MessageLogDAO(BaseDAO[MessageLogModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MessageLogModel)


__all__ = ["MessageLogDAO"]
