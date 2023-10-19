import calendar

from aiogram_dialog import Dialog
from aiogram_dialog import DialogManager
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import NumberedPager
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.text import List

from src.bot.states import DialogSG


async def product_getter(**_kwargs):
    return {
        "products": [(f"Product {i}", i) for i in range(1, 30)],
    }


async def paging_getter(dialog_manager: DialogManager, **_kwargs):
    current_page = await dialog_manager.find("stub_scroll").get_page()
    return {
        "pages": 7,
        "current_page": current_page + 1,
        "day": calendar.day_name[current_page],
    }


MAIN_MENU_BTN = SwitchTo(Const("Main menu"), id="main", state=DialogSG.MAIN)
dialog = Dialog(
    Window(
        Const("Text list scrolling:\n"),
        List(
            Format("{pos}. {item[0]}"),
            items="products",
            id="list_scroll",
            page_size=10,
        ),
        NumberedPager(
            scroll="list_scroll",
        ),
        MAIN_MENU_BTN,
        getter=product_getter,
        state=DialogSG.LIST,
    )
)


__all__ = ["dialog"]
