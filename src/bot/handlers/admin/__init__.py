from aiogram import Router

from .add_channel import add_channel_router
from .scroll_channels import scroll_channel_router


admin_router = Router(name="admin")
admin_router.include_router(add_channel_router)
admin_router.include_router(scroll_channel_router)


__all__ = ["admin_router"]
