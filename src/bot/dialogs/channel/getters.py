from aiogram_dialog import DialogManager

from .constants import ID_STUB_SCROLL
from src.db import DataAccessLayer


async def scroll_getter(dialog_manager: DialogManager, **_kwargs):
    current_page = await dialog_manager.find(ID_STUB_SCROLL).get_page()

    dal: DataAccessLayer = dialog_manager.start_data["dal"]

    channels = await dal.get_channels()

    dialog_manager.dialog_data["channels"] = channels
    dialog_manager.dialog_data["current_page"] = current_page

    return {"is_empty": True if len(channels) == 0 else False, "pages": len(channels)}


__all__ = ["scroll_getter"]
