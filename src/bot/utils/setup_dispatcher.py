from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.memory import SimpleEventIsolation
from structlog.stdlib import BoundLogger


def setup_dispatcher(logger: BoundLogger, chat_id: int) -> Dispatcher:
    """
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
    return dp


__all__ = ["setup_dispatcher"]
