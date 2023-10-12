from abc import ABC
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class Query(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, *args, **kwargs) -> Any:
        raise NotImplementedError()
