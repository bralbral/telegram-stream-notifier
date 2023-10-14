from abc import ABC
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class Repo(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, *args, **kwargs) -> Any:
        raise NotImplementedError()


__all__ = ["Repo"]
