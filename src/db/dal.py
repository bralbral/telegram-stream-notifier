import asyncio
import os
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import SQLITE_DATABASE_FILE_PATH
from .dao import ChannelDAO
from .dao import ChannelTypeDAO
from .dao import MessageLogDAO
from .dao import UserDAO
from .dao import UserRoleDAO
from .exceptions import DatabaseDoesNotExist
from .models import ChannelModel
from .models import MessageLogModel
from .models import UserModel
from .session import session_maker


class DataAccessLayer:
    def __init__(self, session: Optional[AsyncSession] = None) -> None:

        if session is None:
            self.__create_session()
        else:
            self.__session = session

        self.__sqlite_exists()
        self.channel_dao = ChannelDAO(session=self.__session)
        self.channel_type_dao = ChannelTypeDAO(session=self.__session)
        self.message_log_dao = MessageLogDAO(session=self.__session)
        self.user_dao = UserDAO(session=self.__session)
        self.user_role_dao = UserRoleDAO(session=self.__session)

    @staticmethod
    def __sqlite_exists():
        if not os.path.exists(SQLITE_DATABASE_FILE_PATH):
            raise DatabaseDoesNotExist()

    def __create_session(self):
        """
        :return:
        """
        session: AsyncSession = session_maker()
        self.__session = session

    def __del__(self):
        """
        :return:
        """
        if self.__session:
            asyncio.create_task(self.__session.close())

    async def create_user(self, user: UserModel) -> Optional[UserModel]:
        """
        :param user:
        :return:
        """
        return await self.user_dao.create(obj=user)

    async def get_user_by_pk(self, pk: int) -> Optional[UserModel]:
        """
        :param pk:
        :return:
        """
        return await self.user_dao.get_first(id=pk)

    async def get_user_by_attr(self, **kwargs) -> Optional[UserModel]:
        """
        :param kwargs:
        :return:
        """
        return await self.user_dao.get_first(**kwargs)

    async def list_users_by_attr(self, **kwargs) -> list[UserModel]:
        """
        :param kwargs:
        :return:
        """
        return list(await self.user_dao.get_many(**kwargs))

    async def is_superusers_exists(self) -> bool:
        """
        :return:
        """

        return bool(await self.list_users_by_attr(**{"is_superuser": True}))

    async def get_users(self, superusers: bool = False) -> list[int]:
        """
        :param superusers:
        :return:
        """
        users: list[UserModel]
        if superusers:
            users = await self.list_users_by_attr(**{"is_superuser": True})
        else:
            users = await self.list_users_by_attr(**{"is_superuser": False})

        user_ids: list[int] = [user.user_id for user in users]
        return user_ids

    async def get_last_published_message_id(self) -> Optional[int]:
        """
        :return:
        """
        message_log = await self.message_log_dao.get_first()
        if message_log:
            return message_log.message_id

        return None

    async def create_message(self, obj: MessageLogModel) -> Optional[MessageLogModel]:
        """
        :param obj:
        :return:
        """
        return await self.message_log_dao.create(obj=obj)

    async def create_channel(self, obj: ChannelModel) -> Optional[ChannelModel]:
        """
        :return:
        """
        return await self.channel_dao.create(obj=obj)

    async def get_channels(self, **kwargs) -> list[ChannelModel]:
        """
        :param kwargs:
        :return:
        """

        return list(await self.channel_dao.get_many(**kwargs))

    async def delete_channel_by_id(self, id: int) -> Optional[int]:
        """
        :param id:
        :return:
        """
        return await self.channel_dao.delete(id=id)

    async def update_channel_by_id(self, obj: ChannelModel) -> Optional[int]:
        """
        :return:
        """
        return await self.channel_dao.update(obj=obj)

    __all__ = ["DataAccessLayer"]
