from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class ChannelsListSG(StatesGroup):
    scrolling = State()
    delete = State()
    turn_on = State()
    turn_off = State()


class ChannelCreateSG(StatesGroup):
    start = State()
    type_selected = State()
    url_selected = State()


class UsersSG(StatesGroup):
    promote = State()


__all__ = ["ChannelCreateSG", "ChannelsListSG", "UsersSG"]
