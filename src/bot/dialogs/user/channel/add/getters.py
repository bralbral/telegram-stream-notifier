from aiogram_dialog import DialogManager

from src.db import DataAccessLayer
from src.db.models.channel_type import ChannelType


async def select_channel_type_window_getter(dialog_manager: DialogManager, **kwargs):

    dal: DataAccessLayer = dialog_manager.start_data["dal"]

    channels = await dal.get_channels()

    dialog_manager.dialog_data["channels"] = channels
    dialog_manager.dialog_data["channel_types"] = ChannelType.list()

    return {
        "channel_types": dialog_manager.dialog_data["channel_types"],
    }


__all__ = ["select_channel_type_window_getter"]
