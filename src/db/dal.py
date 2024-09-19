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
from .models import UserModel
from .session import session_maker


class DataAccessLayer:
    def __init__(self, session: Optional[AsyncSession] = None) -> None:
        if session is None:
            self.__create_session()
        else:
            self.__session = session

        self.__sqlite_exists()
        self.channel_dao = ChannelDAO(session=session)
        self.channel_type_dao = ChannelTypeDAO(session=session)
        self.message_log_dao = MessageLogDAO(session=session)
        self.user_dao = UserDAO(session=session)
        self.user_role_dao = UserRoleDAO(session=session)

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
        return await self.user_dao.get_by_id(id=pk)

    async def get_user_by_attr(self, **kwargs) -> Optional[UserModel]:
        """
        :param kwargs:
        :return:
        """
        return await self.user_dao.get(**kwargs)

    async def list_users_by_attr(self, **kwargs) -> list[UserRetrieveDTO]:
        """
        :param kwargs:
        :return:
        """
        users: list[UserRetrieveDTO] = cast(
            list[UserRetrieveDTO], await self.__user_repo.list_by_attrs(**kwargs)
        )
        return users

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
        users: list[UserRetrieveDTO]
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
        message_log_dto: Optional[MessageLogRetrieveDTO] = (
            await self.__message_log_repo.get_by_attr()
        )
        if message_log_dto:
            return message_log_dto.message_id

        return None

    async def create_message(
        self, message_log_schema: MessageLogCreateDTO
    ) -> Optional[MessageLogRetrieveDTO]:
        """
        :param message_log_schema:
        :return:
        """
        return await self.__message_log_repo.create(
            message_log_schema=message_log_schema
        )

    async def create_channel(
        self, channel_schema: ChannelCreateDTO
    ) -> Optional[ChannelRetrieveDTO]:
        """
        :param channel_schema:
        :return:
        """
        return await self.__channel_repo.create(channel_schema=channel_schema)

    async def get_channels(self, **kwargs) -> list[ChannelRetrieveDTO]:
        """
        :param kwargs:
        :return:
        """
        channels: list[ChannelRetrieveDTO] = cast(
            list[ChannelRetrieveDTO], await self.__channel_repo.list_by_attrs(**kwargs)
        )

        return channels

    async def delete_channel_by_id(self, _id: int) -> Optional[int]:
        """
        :param _id:
        :return:
        """
        return await self.__channel_repo.delete_by_pk(pk=_id)

    async def update_channel_by_id(self, _id: int, data: dict) -> Optional[int]:
        """
        :param data:
        :param _id:
        :return:
        """
        return await self.__channel_repo.update_by_pk(pk=_id, data=data)

    __all__ = ["DataAccessLayer"]
