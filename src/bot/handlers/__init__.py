from aiogram import Dispatcher

from .admin import admin_router
from .common import router as common_router
from .user import user_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(common_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)


__all__ = ["register_handlers"]
