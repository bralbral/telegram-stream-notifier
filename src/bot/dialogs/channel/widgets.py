from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Format


class Viewer(Format):
    async def _render_text(
        self,
        data: dict,
        manager: DialogManager,
    ) -> Any:
        text: str = self.text.replace("{current_page}", str(data["current_page"]))
        return text.format_map(data)


__all__ = ["Viewer"]
