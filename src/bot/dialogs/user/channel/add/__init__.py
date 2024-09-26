from aiogram_dialog import Dialog
from aiogram_dialog import LaunchMode

from .windows import label_handler_window
from .windows import select_channel_type_window
from .windows import url_handler_window

channel_create_dialog = Dialog(
    select_channel_type_window(),
    url_handler_window(),
    label_handler_window(),
    launch_mode=LaunchMode.STANDARD,
)


__all__ = ["channel_create_dialog"]
