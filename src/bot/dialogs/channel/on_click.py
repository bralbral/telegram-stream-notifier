from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram_dialog import (
    DialogManager,
)
from aiogram_dialog.widgets.kbd import (
    Button,
)

from src.bot.states import ChannelDialogSG
from src.db import DataAccessLayer
from src.schemas import ChannelSchema


async def on_finish(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if manager.has_context():
        with suppress(TelegramBadRequest):
            await callback.message.delete()

        await manager.done()


async def on_delete(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(ChannelDialogSG.delete)


async def on_perform_delete(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    index = manager.dialog_data["current_page"]
    channel: ChannelSchema = manager.dialog_data["channels"][index]

    if channel.id:
        dal: DataAccessLayer = manager.start_data["dal"]
        result = await dal.delete_channel_by_id(_id=channel.id)

        if result:
            await callback.answer("Success.")
        else:
            await callback.answer("Cannot delete row.")
    else:
        await callback.answer("Cannot delete row.")

    await manager.switch_to(state=ChannelDialogSG.scrolling)


async def on_turn_off(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(ChannelDialogSG.turn_off)


async def on_turn_on(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(ChannelDialogSG.turn_on)


__all__ = ["on_delete", "on_finish", "on_perform_delete", "on_turn_off", "on_turn_on"]
