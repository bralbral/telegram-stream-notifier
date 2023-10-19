from aiogram import Dispatcher

from .admin import router as admin_router
from .superuser import router as super_user_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(super_user_router)
    dp.include_router(admin_router)


__all__ = ["register_handlers"]
