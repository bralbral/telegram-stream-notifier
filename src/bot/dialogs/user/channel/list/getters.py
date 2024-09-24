from aiogram_dialog import DialogManager

from .constants import ID_STUB_SCROLL
from src.bot.filters import UserRole
from src.db import DataAccessLayer


async def scroll_getter(dialog_manager: DialogManager, **_kwargs):
    current_page = await dialog_manager.find(ID_STUB_SCROLL).get_page()

    dal: DataAccessLayer = dialog_manager.start_data["dal"]
    role: UserRole = dialog_manager.start_data["role"]

    channels = await dal.get_channels()

    dialog_manager.dialog_data["channels"] = channels
    dialog_manager.dialog_data["current_page"] = current_page

    return {
        "role": role,
        "is_empty": True if len(channels) == 0 else False,
        "pages": len(channels),
        "channels": [channel.to_html() for channel in channels],
        "current_page": current_page,
    }


__all__ = ["scroll_getter"]
