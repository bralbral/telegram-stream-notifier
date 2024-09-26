from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram_dialog import (
    DialogManager,
)
from aiogram_dialog.widgets.kbd import (
    Button,
)

from src.bot.states import ChannelsListSG
from src.db import DataAccessLayer
from src.db.models import ChannelModel


async def on_finish(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if manager.has_context():
        with suppress(TelegramBadRequest):
            await callback.message.delete()

        await manager.done()


async def on_delete(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(ChannelsListSG.delete)


async def on_perform_delete(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    index = manager.dialog_data["current_page"]
    channel: ChannelModel = manager.dialog_data["channels"][index]

    if channel.id:
        dal: DataAccessLayer = manager.start_data["dal"]
        result = await dal.delete_channel_by_id(id=channel.id)

        if result:
            await callback.answer("Success.")
        else:
            await callback.answer("Cannot delete row.")
    else:
        await callback.answer("Cannot delete row.")

    await manager.switch_to(state=ChannelsListSG.scrolling)


async def on_turn_off(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(ChannelsListSG.turn_off)


async def on_turn_on(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(ChannelsListSG.turn_on)


async def on_perform_update(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    index = manager.dialog_data["current_page"]
    channel: ChannelModel = manager.dialog_data["channels"][index]

    if channel.id:
        dal: DataAccessLayer = manager.start_data["dal"]

        data = callback.data
        if data == "on":
            enabled = True
        elif data == "off":
            enabled = False
        else:
            await callback.answer("Unknown callback data")
            return

        channel_obj = await dal.channel_dao.get_first(**{"id": channel.id})

        if not channel_obj:
            await callback.answer(
                "❌ Channel does not exist. Please contact administrator."
            )
            return

        channel_obj.enabled = enabled
        result = await dal.update_channel_by_id(obj=channel_obj)

        if result:
            await callback.answer("Success.")
        else:
            await callback.answer("Cannot update row.")
    else:
        await callback.answer("Cannot update row.")

    await manager.switch_to(state=ChannelsListSG.scrolling)


__all__ = [
    "on_delete",
    "on_finish",
    "on_perform_delete",
    "on_perform_update",
    "on_turn_off",
    "on_turn_on",
]
