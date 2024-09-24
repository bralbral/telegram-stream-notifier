from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.text import Multi
from sulguk import SULGUK_PARSE_MODE

from .getters import label_handler_window_getter
from .getters import select_channel_type_window_getter
from .getters import url_handler_window_getter
from .handlers import label_handler
from .handlers import url_handler
from .on_click import on_finish
from .on_click import on_select_channel_type
from src.bot.states import ChannelCreateSG


def select_channel_type_window():
    return Window(
        Const(
            "Select channel type",
        ),
        Select(
            Format("{item}"),
            items="channel_types",
            item_id_getter=lambda x: x,
            id="channel_types",
            on_click=on_select_channel_type,
        ),
        Button(Const("❌ Exit"), id="finish", on_click=on_finish),
        state=ChannelCreateSG.start,
        getter=select_channel_type_window_getter,
        parse_mode=SULGUK_PARSE_MODE,
    )


def url_handler_window():
    return Window(
        Multi(
            Const(
                "✅ OK, now you can set the <b>URL</b>. Please use the template below"
            ),
            Format("<b>{url_example}</b>"),
            sep="<br/>",
        ),
        MessageInput(url_handler, content_types=[ContentType.TEXT]),
        Button(Const("❌ Exit"), id="finish", on_click=on_finish),
        state=ChannelCreateSG.type_selected,
        getter=url_handler_window_getter,
        parse_mode=SULGUK_PARSE_MODE,
    )


def label_handler_window():
    return Window(
        Multi(
            Format(
                "URL set to <b>{url}</b>, enter display name or <b>/cancel</b> for reject"
            ),
            sep="<br/>",
        ),
        MessageInput(label_handler, content_types=[ContentType.TEXT]),
        Button(Const("❌ Exit"), id="finish", on_click=on_finish),
        state=ChannelCreateSG.url_selected,
        getter=label_handler_window_getter,
        parse_mode=SULGUK_PARSE_MODE,
    )


__all__ = ["label_handler_window", "select_channel_type_window", "url_handler_window"]
