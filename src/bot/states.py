from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class ChannelDialogSG(StatesGroup):
    input_url = State()
    input_label = State()
    scrolling = State()
    delete = State()
    turn_on = State()
    turn_off = State()


__all__ = ["ChannelDialogSG"]
