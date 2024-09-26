from aiogram import Dispatcher

from .channel import channel_create_dialog
from .channel import channels_list_dialog


def register_user_dialogs(dp: Dispatcher) -> None:
    dp.include_router(channel_create_dialog)
    dp.include_router(channels_list_dialog)


__all__ = ["register_user_dialogs"]
