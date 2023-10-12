from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.memory import SimpleEventIsolation
from sqlalchemy.ext.asyncio import async_sessionmaker
from structlog.stdlib import BoundLogger

from ..middlewares import setup_middlewares


def setup_dispatcher(
    logger: BoundLogger, chat_id: int, session_maker: async_sessionmaker
) -> Dispatcher:
    """
    :param session_maker:
    :param logger:
    :param chat_id:
    :return:
    """
    dp: Dispatcher = Dispatcher(
        storage=MemoryStorage(),
        logger=logger,
        chat_id=chat_id,
        events_isolation=SimpleEventIsolation(),
    )

    setup_middlewares(dp=dp, session_maker=session_maker)

    return dp


__all__ = ["setup_dispatcher"]
