from aiogram import Dispatcher

from src.db import DataAccessLayer


def setup_dispatcher(chat_id: int, dal: DataAccessLayer, scheduler) -> Dispatcher:
    dp = Dispatcher()

    from .handlers import register_handlers

    register_handlers(dp)

    return dp


__all__ = ["setup_dispatcher"]
