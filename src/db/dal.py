import asyncio
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas import UserSchema
from .repo import ChannelRepo
from .repo import UserRepo
from .session import session_maker


class DataAccessLayer:
    def __init__(self, session: Optional[AsyncSession] = None) -> None:
        if session is None:
            self.__create_session()
        else:
            self.__session = session

        self.__init_repo()

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
        self.__user_repo = UserRepo(session=self.__session)
        self.__channel_repo = ChannelRepo(session=self.__session)

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
        return await self.__user_repo.list_by_attrs(**kwargs)

    async def is_superusers_exists(self) -> bool:
        """
        :return:
        """

        return bool(await self.list_users_by_attr(**{"is_superuser": True}))

    async def get_admins_or_superusers(self, superusers: bool = False) -> list[int]:
        """
        :return:
        """
        users: list[UserSchema]
        if superusers:
            users = await self.list_users_by_attr(**{"is_superuser": True})
        else:
            users = await self.list_users_by_attr(**{"is_admin": True})

        user_ids: list[int] = [user.user_id for user in users]
        return user_ids


__all__ = ["DataAccessLayer"]
