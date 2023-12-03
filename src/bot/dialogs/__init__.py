from aiogram import Dispatcher

from .channel import channel_dialog


def register_dialogs(dp: Dispatcher) -> None:
    dp.include_router(channel_dialog)


__all__ = ["register_dialogs"]
