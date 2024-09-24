from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.text import Format
from sulguk import SULGUK_PARSE_MODE

from .getters import select_channel_type_window_getter
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


#
#
# SWITCH_TO_SCROLLING = SwitchTo(
#     text=Const("🔙 No, return me back."), state=ChannelsSG.scrolling, id="back"
# )
#
#
# dialog = Dialog(
#     Window(
#         Const("Greetings! Please, introduce yourself:"),
#         StaticMedia(
#             path=os.path.join(src_dir, "python_logo.png"),
#             type=ContentType.PHOTO,
#         ),
#         MessageInput(name_handler, content_types=[ContentType.TEXT]),
#         MessageInput(other_type_handler),
#         state=DialogSG.greeting,
#     ),
#     Window(
#         Format("{name}! How old are you?"),
#         Select(
#             Format("{item}"),
#             items=["0-12", "12-18", "18-25", "25-40", "40+"],
#             item_id_getter=lambda x: x,
#             id="w_age",
#             on_click=on_age_changed,
#         ),
#         state=DialogSG.age,
#         getter=get_data,
#         preview_data={"name": "Tishka17"},
#     ),
#     Window(
#         Multi(
#             Format("{name}! Thank you for your answers."),
#             Const("Hope you are not smoking", when="can_smoke"),
#             sep="\n\n",
#         ),
#         Row(
#             Back(),
#             SwitchTo(Const("Restart"), id="restart", state=DialogSG.greeting),
#             Button(Const("Finish"), on_click=on_finish, id="finish"),
#         ),
#         getter=get_data,
#         state=DialogSG.finish,
#     ),
# )
#
#
#
# def select_url_window():
#     return Window(
#         Const("Are you sure?"),
#         Row(
#             Button(
#                 Const("✅ Yes, delete this channel_listing."),
#                 id="delete",
#                 on_click=on_perform_delete,
#             ),
#             SWITCH_TO_SCROLLING,
#         ),
#         Button(Const("❌ Exit"), id="finish", on_click=on_finish),
#         state=ChannelsSG.delete,
#         getter=scroll_getter,
#     )
#
#
# def turn_on_window():
#     return Window(
#         Const("Are you sure?"),
#         Row(
#             Button(
#                 Const("✅ Yes, turn on this channel_listing."),
#                 id="on",
#                 on_click=on_perform_update,
#             ),
#             SWITCH_TO_SCROLLING,
#         ),
#         Button(Const("❌ Exit"), id="finish", on_click=on_finish),
#         state=ChannelsSG.turn_on,
#         getter=scroll_getter,
#     )
#
#
# def turn_off_window():
#     return Window(
#         Const("Are you sure?"),
#         Row(
#             Button(
#                 Const("✅ Yes, turn off this channel_listing."),
#                 id="off",
#                 on_click=on_perform_update,
#             ),
#             SWITCH_TO_SCROLLING,
#         ),
#         Button(Const("❌ Exit"), id="finish", on_click=on_finish),
#         state=ChannelsSG.turn_off,
#         getter=scroll_getter,
#     )


__all__ = ["select_channel_type_window"]
