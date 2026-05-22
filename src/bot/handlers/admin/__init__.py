from aiogram import Router

from .add_user import add_user_router
from .scheduler import scheduler_router

admin_router = Router(name="admin")
admin_router.include_router(add_user_router)
admin_router.include_router(scheduler_router)


__all__ = ["admin_router"]
