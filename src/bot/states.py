from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class DialogSG(StatesGroup):
    MAIN = State()
    DEFAULT_PAGER = State()
    PAGERS = State()
    LIST = State()
    TEXT = State()
    STUB = State()


__all__ = ["DialogSG"]
