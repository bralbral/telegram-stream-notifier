from aiogram_dialog import Dialog
from aiogram_dialog import LaunchMode

from .windows import delete_window
from .windows import scroll_window
from .windows import turn_off_window
from .windows import turn_on_window

channel_dialog = Dialog(
    scroll_window(),
    delete_window(),
    turn_on_window(),
    turn_off_window(),
    launch_mode=LaunchMode.STANDARD,
)


__all__ = ["channel_dialog"]
