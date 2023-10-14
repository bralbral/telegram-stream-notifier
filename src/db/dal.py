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
        session: AsyncSession = session_maker()
        self.__session = session

    def __del__(self):
        if self.__session:
            asyncio.create_task(self.__session.close())

    def __init_repo(self) -> None:
        self.__user_repo = UserRepo(session=self.__session)
        self.__channel_repo = ChannelRepo(session=self.__session)

    async def is_superusers_exists(self) -> bool:
        return bool(await self.__user_repo.get_superusers())

    async def create_user(self, user_schema: UserSchema) -> Optional[UserSchema]:
        return await self.__user_repo.create(user_schema=user_schema)

    async def get_user_by_pk(self, pk: int) -> Optional[UserSchema]:
        return await self.__user_repo.get_by_pk(pk=pk)

    async def get_user_by_attr(self, **kwargs) -> Optional[UserSchema]:
        return await self.__user_repo.get_by_attr(**kwargs)


__all__ = ["DataAccessLayer"]
