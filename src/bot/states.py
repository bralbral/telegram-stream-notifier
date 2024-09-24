from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class ChannelsSG(StatesGroup):
    input_url = State()
    input_label = State()
    scrolling = State()
    delete = State()
    turn_on = State()
    turn_off = State()
    bulk_channels = State()


class ChannelCreateSG(StatesGroup):
    start = State()
    type_selected = State()
    url_selected = State()


class UsersSG(StatesGroup):
    promote = State()


__all__ = ["ChannelCreateSG", "ChannelsSG", "UsersSG"]
