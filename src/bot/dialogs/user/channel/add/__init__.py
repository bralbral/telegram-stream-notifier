from aiogram_dialog import Dialog
from aiogram_dialog import LaunchMode

from .windows import select_channel_type_window

channel_create_dialog = Dialog(
    select_channel_type_window(),
    launch_mode=LaunchMode.STANDARD,
)


__all__ = ["channel_create_dialog"]
