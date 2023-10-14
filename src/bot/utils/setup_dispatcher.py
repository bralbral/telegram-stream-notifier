from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.memory import SimpleEventIsolation

from ...db import DataAccessLayer
from ..handlers import register_handlers
from ..middlewares import register_middlewares


def setup_dispatcher(chat_id: int, dal: DataAccessLayer) -> Dispatcher:
    """
    :param dal:
    :param chat_id:
    :return:
    """
    dp: Dispatcher = Dispatcher(
        storage=MemoryStorage(),
        chat_id=chat_id,
        events_isolation=SimpleEventIsolation(),
    )

    register_middlewares(dp=dp, dal=dal)
    register_handlers(dp=dp)

    return dp


__all__ = ["setup_dispatcher"]
