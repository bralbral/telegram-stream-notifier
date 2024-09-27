from contextlib import suppress
from typing import Any

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram_dialog import ChatEvent
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import (
    Button,
)

from src.db.models.channel_type import ChannelType


async def on_finish(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if manager.has_context():
        with suppress(TelegramBadRequest):
            await callback.message.delete()

        await manager.done()


async def on_select_channel_type(
    callback: ChatEvent,
    select: Any,
    manager: DialogManager,
    item_id: str,
):
    # temporary stub
    # wait for https://github.com/bralbral/telegram-stream-notifier/issues/114
    if item_id == ChannelType.KICK:
        await callback.answer(
            "Notifications from Kick.com do not implemented. Try later."
        )
        return

    manager.dialog_data["selected_channel_type"] = item_id
    await manager.next()


__all__ = [
    "on_finish",
    "on_select_channel_type",
]
