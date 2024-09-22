from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from src.db.models import ChannelTypeModel


class ChannelTypeDAO(BaseDAO[ChannelTypeModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ChannelTypeModel)


__all__ = ["ChannelTypeDAO"]
