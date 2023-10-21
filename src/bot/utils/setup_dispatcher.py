from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram_dialog import setup_dialogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ...db import DataAccessLayer
from ..dialogs import register_dialogs
from ..handlers import register_handlers
from ..middlewares import register_middlewares


def setup_dispatcher(
    chat_id: int, dal: DataAccessLayer, scheduler: AsyncIOScheduler
) -> Dispatcher:
    """
    :param scheduler:
    :param dal:
    :param chat_id:
    :return:
    """
    dp: Dispatcher = Dispatcher(
        storage=MemoryStorage(),
        scheduler=scheduler,
        chat_id=chat_id,
        events_isolation=SimpleEventIsolation(),
    )

    register_middlewares(dp=dp, dal=dal)
    register_handlers(dp=dp)
    register_dialogs(dp=dp)
    setup_dialogs(dp)

    return dp


__all__ = ["setup_dispatcher"]
