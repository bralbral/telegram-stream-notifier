import asyncio
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .repo import ChannelRepo
from .repo import UserRepo
from .session import session_maker


class DataAccessLayer:
    def __init__(self, session: Optional[AsyncSession] = None) -> None:
        if session is None:
            self.__create_session()
        else:
            self.session = session

        self.__init_repo()

    def __create_session(self):
        session: AsyncSession = session_maker()
        self.session = session

    def __del__(self):
        if self.session:
            asyncio.create_task(self.session.close())

    def __init_repo(self) -> None:
        self.user_repo = UserRepo(session=self.session)
        self.channel_repo = ChannelRepo(session=self.session)

    async def check_superusers(self) -> bool:
        return bool(await self.user_repo.get_superusers())


__all__ = ["DataAccessLayer"]
