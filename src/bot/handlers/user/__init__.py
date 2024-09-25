from aiogram import Router

from .add_channel import add_channel_router
from .list_channels import list_channels_router


user_router = Router(name="user")
user_router.include_router(add_channel_router)
user_router.include_router(list_channels_router)


__all__ = ["user_router"]
