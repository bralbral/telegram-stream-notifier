from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ....db import DataAccessLayer
from ...filters import RoleFilter
from ...filters import UserRole

list_channels_router = Router(name="list_channels")


@list_channels_router.message(
    Command("channels"),
    RoleFilter(role=[UserRole.USER, UserRole.ADMIN]),
)
async def list_channels(message: Message, dal: DataAccessLayer, **kwargs) -> None:
    from_user = message.from_user
    if not from_user:
        await message.answer("❌ User not found.")
        return
    user = await dal.get_user_by_attr(user_id=from_user.id)
    if not user:
        await message.answer("❌ User not found.")
        return

    channels = await user.subscribed_channels.all()
    if not channels:
        await message.answer(
            "You have no subscribed channels. Use /add_channel <url> [label]"
        )
        return

    text = "📺 Your channels:\n\n"
    for ch in channels:
        status = "✅" if ch.enabled else "❌"
        text += f"{status} <b>{ch.label}</b> - {ch.url}\n"

    await message.answer(text)


__all__ = ["list_channels_router"]
