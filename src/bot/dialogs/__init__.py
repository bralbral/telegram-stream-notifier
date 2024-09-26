from aiogram import Dispatcher

from .user import register_user_dialogs


def register_dialogs(dp: Dispatcher) -> None:
    register_user_dialogs(dp=dp)


__all__ = ["register_dialogs"]
