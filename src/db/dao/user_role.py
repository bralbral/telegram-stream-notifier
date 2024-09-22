from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from src.db.models import UserRoleModel


class UserRoleDAO(BaseDAO[UserRoleModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserRoleModel)


__all__ = ["UserRoleDAO"]
