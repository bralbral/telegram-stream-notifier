from aiogram import Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog.api.exceptions import UnknownIntent

from .common import router as common_router
from .errors import on_unknown_intent
from .superuser import superuser_router
from .user import user_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(common_router)
    dp.include_router(superuser_router)
    dp.include_router(user_router)
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )


__all__ = ["register_handlers"]
