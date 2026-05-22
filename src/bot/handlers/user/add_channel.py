from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ....db import DataAccessLayer
from ....db.models import ChannelModel
from ...filters import RoleFilter
from ...filters import UserRole
from src.scheduler.utils import detect_platform

add_channel_router = Router(name="add_channel")


@add_channel_router.message(
    Command("add_channel"),
    RoleFilter(role=[UserRole.USER, UserRole.ADMIN]),
)
async def add_channel(message: Message, dal: DataAccessLayer, **kwargs) -> None:
    text = message.text
    if not text:
        await message.answer("Usage: /add_channel <url>")
        return
    parts = text.split(maxsplit=2)
    if len(parts) < 2:
        await message.answer("Usage: /add_channel <url>")
        return

    url = parts[1].strip()
    label = url.split("/")[-1]

    platform = detect_platform(url)
    if not platform:
        await message.answer(f"❌ Cannot detect platform for URL: {url}")
        return

    existing = await dal.channel_dao.get_first(url=url)
    if existing:
        await message.answer(f"❌ Channel {url} already exists.")
        return

    from_user = message.from_user
    if not from_user:
        await message.answer("❌ User not found.")
        return
    user = await dal.get_user_by_attr(user_id=from_user.id)
    if not user:
        await message.answer("❌ User not found. Contact admin.")
        return

    channel_type, _ = await dal.channel_type_dao.get_or_create(type=platform)

    channel = ChannelModel(
        url=url,
        label=label,
        enabled=True,
        creator=user,
        type=channel_type,
    )
    result = await dal.create_channel(obj=channel)

    if result:
        await result.subscribers.add(user)
        await message.answer("✅ Channel added! Notifications will be sent here.")
    else:
        await message.answer("❌ Failed to add channel.")


__all__ = ["add_channel_router"]
