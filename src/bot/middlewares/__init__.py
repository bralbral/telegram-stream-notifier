from aiogram import Dispatcher

from .dal import DataAccessLayerMiddleware
from .role import RoleMiddleware
from src.db import DataAccessLayer


def register_middlewares(dp: Dispatcher, dal: DataAccessLayer) -> None:
    dp.message.outer_middleware(DataAccessLayerMiddleware(dal=dal))
    dp.message.outer_middleware(RoleMiddleware())


__all__ = ["register_middlewares"]
