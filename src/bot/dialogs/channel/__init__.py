from aiogram_dialog import Dialog
from aiogram_dialog import LaunchMode

from .windows import delete_window
from .windows import scroll_window

dialog = Dialog(
    scroll_window(),
    delete_window(),
    launch_mode=LaunchMode.STANDARD,
)


__all__ = ["dialog"]
