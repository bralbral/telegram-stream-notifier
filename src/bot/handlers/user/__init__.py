from aiogram import Router

from .add_channel import add_channel_router
from .scroll_channels import scroll_channel_router


user_router = Router(name="user")
user_router.include_router(add_channel_router)
user_router.include_router(scroll_channel_router)


__all__ = ["user_router"]
