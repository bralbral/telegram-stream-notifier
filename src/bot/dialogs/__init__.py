from aiogram import Dispatcher

from .channel import dialog


def register_dialogs(dp: Dispatcher) -> None:
    dp.include_router(dialog)


__all__ = ["register_dialogs"]
