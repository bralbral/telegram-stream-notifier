from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram_dialog import (
    DialogManager,
)
from aiogram_dialog.widgets.kbd import (
    Button,
)

from src.bot.states import ChannelsSG
from src.db import DataAccessLayer
from src.dto import ChannelRetrieveDTO


async def on_finish(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if manager.has_context():
        with suppress(TelegramBadRequest):
            await callback.message.delete()

        await manager.done()


async def on_delete(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(ChannelsSG.delete)


async def on_perform_delete(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    index = manager.dialog_data["current_page"]
    channel: ChannelRetrieveDTO = manager.dialog_data["channels"][index]

    if channel.id:
        dal: DataAccessLayer = manager.start_data["dal"]
        result = await dal.delete_channel_by_id(_id=channel.id)

        if result:
            await callback.answer("Success.")
        else:
            await callback.answer("Cannot delete row.")
    else:
        await callback.answer("Cannot delete row.")

    await manager.switch_to(state=ChannelsSG.scrolling)


async def on_turn_off(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(ChannelsSG.turn_off)


async def on_turn_on(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(ChannelsSG.turn_on)


async def on_perform_update(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    index = manager.dialog_data["current_page"]
    channel: ChannelRetrieveDTO = manager.dialog_data["channels"][index]

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

        result = await dal.update_channel_by_id(
            _id=channel.id, data={"enabled": enabled}
        )

        if result:
            await callback.answer("Success.")
        else:
            await callback.answer("Cannot update row.")
    else:
        await callback.answer("Cannot update row.")

    await manager.switch_to(state=ChannelsSG.scrolling)


__all__ = [
    "on_delete",
    "on_finish",
    "on_perform_delete",
    "on_perform_update",
    "on_turn_off",
    "on_turn_on",
]
