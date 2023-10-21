import asyncio
import os
from typing import cast
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import SQLITE_DATABASE_FILE_PATH
from ..schemas import ChannelSchema
from ..schemas import MessageLogSchema
from ..schemas import UserSchema
from .exceptions import DatabaseDoesNotExist
from .models import ChannelOrm
from .models import MessageLogOrm
from .models import UserOrm
from .repo import ChannelRepo
from .repo import MessageLogRepo
from .repo import UserRepo
from .session import session_maker


class DataAccessLayer:
    def __init__(self, session: Optional[AsyncSession] = None) -> None:
        if session is None:
            self.__create_session()
        else:
            self.__session = session

        self.__sqlite_exists()
        self.__init_repo()

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

    def __init_repo(self) -> None:
        """
        :return:
        """
        self.__user_repo = UserRepo(
            session=self.__session, schema=UserSchema, model_orm=UserOrm
        )
        self.__channel_repo = ChannelRepo(
            session=self.__session,
            schema=ChannelSchema,
            model_orm=ChannelOrm,
        )
        self.__message_log_repo = MessageLogRepo(
            session=self.__session,
            schema=MessageLogSchema,
            model_orm=MessageLogOrm,
        )

    async def create_user(self, user_schema: UserSchema) -> Optional[UserSchema]:
        """
        :param user_schema:
        :return:
        """
        return await self.__user_repo.create(user_schema=user_schema)

    async def get_user_by_pk(self, pk: int) -> Optional[UserSchema]:
        """
        :param pk:
        :return:
        """
        return await self.__user_repo.get_by_pk(pk=pk)

    async def get_user_by_attr(self, **kwargs) -> Optional[UserSchema]:
        """
        :param kwargs:
        :return:
        """
        return await self.__user_repo.get_by_attr(**kwargs)

    async def list_users_by_attr(self, **kwargs) -> list[UserSchema]:
        """
        :param kwargs:
        :return:
        """
        users: list[UserSchema] = cast(
            list[UserSchema], await self.__user_repo.list_by_attrs(**kwargs)
        )
        return users

    async def is_superusers_exists(self) -> bool:
        """
        :return:
        """

        return bool(await self.list_users_by_attr(**{"is_superuser": True}))

    async def get_admins_or_superusers(self, superusers: bool = False) -> list[int]:
        """
        :param superusers:
        :return:
        """
        users: list[UserSchema]
        if superusers:
            users = await self.list_users_by_attr(**{"is_superuser": True})
        else:
            users = await self.list_users_by_attr(**{"is_admin": True})

        user_ids: list[int] = [user.user_id for user in users]
        return user_ids

    async def get_last_published_message_id(self) -> Optional[int]:
        """
        :return:
        """
        message_log_dto: Optional[
            MessageLogSchema
        ] = await self.__message_log_repo.get_by_attr()
        if message_log_dto:
            return message_log_dto.message_id

        return None

    async def create_message(
        self, message_log_schema: MessageLogSchema
    ) -> Optional[MessageLogSchema]:
        """
        :param message_log_schema:
        :return:
        """
        return await self.__message_log_repo.create(
            message_log_schema=message_log_schema
        )

    async def create_channel(
        self, channel_schema: ChannelSchema
    ) -> Optional[ChannelSchema]:
        """
        :param channel_schema:
        :return:
        """
        return await self.__channel_repo.create(channel_schema=channel_schema)

    async def get_channels(self, **kwargs) -> list[ChannelSchema]:
        """
        :param kwargs:
        :return:
        """
        channels: list[ChannelSchema] = cast(
            list[ChannelSchema], await self.__channel_repo.list_by_attrs(**kwargs)
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
