from aiogram import Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog.api.exceptions import UnknownIntent

from .admin import router as admin_router
from .core import router as core_router
from .errors import on_unknown_intent
from .superuser import router as super_user_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(core_router)
    dp.include_router(super_user_router)
    dp.include_router(admin_router)
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )


__all__ = ["register_handlers"]
