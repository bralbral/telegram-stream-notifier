from aiogram_dialog import DialogManager

from .constants import url_examples
from .constants import url_validators
from src.db import DataAccessLayer
from src.db.models.channel_type import ChannelType


async def select_channel_type_window_getter(dialog_manager: DialogManager, **kwargs):

    dal: DataAccessLayer = dialog_manager.start_data["dal"]

    channels = await dal.get_channels()

    dialog_manager.dialog_data["dal"] = dal
    dialog_manager.dialog_data["channels"] = channels
    dialog_manager.dialog_data["channel_types"] = ChannelType.list()

    return {
        "channel_types": dialog_manager.dialog_data["channel_types"],
    }


async def url_handler_window_getter(dialog_manager: DialogManager, **kwargs):

    selected_channel_type = dialog_manager.dialog_data["selected_channel_type"]
    url_validator = url_validators[selected_channel_type]
    url_example = url_examples[selected_channel_type]

    dialog_manager.dialog_data["url_validator"] = url_validator
    dialog_manager.dialog_data["url_example"] = url_example

    return {"url_example": url_example}


async def label_handler_window_getter(dialog_manager: DialogManager, **kwargs):

    return {"url": dialog_manager.dialog_data["url"]}


__all__ = [
    "label_handler_window_getter",
    "select_channel_type_window_getter",
    "url_handler_window_getter",
]
