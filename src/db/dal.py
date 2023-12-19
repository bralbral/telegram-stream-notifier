import asyncio
import os
from typing import cast
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..constants import SQLITE_DATABASE_FILE_PATH
from ..dto import ChannelCreateDTO
from ..dto import ChannelErrorCreateDTO
from ..dto import ChannelErrorRetrieveDTO
from ..dto import ChannelRetrieveDTO
from ..dto import MessageLogCreateDTO
from ..dto import MessageLogRetrieveDTO
from ..dto import UserCreateDTO
from ..dto import UserRetrieveDTO
from .dao import ChannelDAO
from .dao import ChannelErrorDAO
from .dao import MessageLogDAO
from .dao import UserRepo
from .exceptions import DatabaseDoesNotExist
from .models import ChannelErrorORM
from .models import ChannelORM
from .models import MessageLogORM
from .models import UserORM
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
            session=self.__session, schema=UserRetrieveDTO, model_orm=UserORM
        )
        self.__channel_repo = ChannelDAO(
            session=self.__session,
            schema=ChannelRetrieveDTO,
            model_orm=ChannelORM,
        )
        self.__channel_error_repo = ChannelErrorDAO(
            session=self.__session,
            schema=ChannelErrorRetrieveDTO,
            model_orm=ChannelErrorORM,
        )
        self.__message_log_repo = MessageLogDAO(
            session=self.__session,
            schema=MessageLogRetrieveDTO,
            model_orm=MessageLogORM,
        )

    async def create_user(
        self, user_schema: UserCreateDTO
    ) -> Optional[UserRetrieveDTO]:
        """
        :param user_schema:
        :return:
        """
        return await self.__user_repo.create(user_schema=user_schema)

    async def get_user_by_pk(self, pk: int) -> Optional[UserRetrieveDTO]:
        """
        :param pk:
        :return:
        """
        return await self.__user_repo.get_by_pk(pk=pk)

    async def get_user_by_attr(self, **kwargs) -> Optional[UserRetrieveDTO]:
        """
        :param kwargs:
        :return:
        """
        return await self.__user_repo.get_by_attr(**kwargs)

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
        message_log_dto: Optional[
            MessageLogRetrieveDTO
        ] = await self.__message_log_repo.get_by_attr()
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

    async def create_channel_error(
        self, channel_error_schema: ChannelErrorCreateDTO
    ) -> int:
        """
        :param channel_error_schema:
        :return:
        """
        return await self.__channel_error_repo.create(
            channel_error_schema=channel_error_schema
        )

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

    async def auto_turn_off_channels(self, errors_limit: int) -> None:
        """
        :return:
        """
        channel_ids = await self.__channel_error_repo.get_channel_ids_with_errors_upper_then_limit(
            limit=errors_limit
        )

        for channel_id in channel_ids:
            await self.update_channel_by_id(_id=channel_id, data={"enabled": False})

        return

    async def clear_channel_errors(self, channel_id: int) -> list[int]:
        return await self.__channel_error_repo.delete_by_attr(
            **{"channel_id": channel_id}
        )


__all__ = ["DataAccessLayer"]
