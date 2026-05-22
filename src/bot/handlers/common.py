from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..filters import RoleFilter
from ..filters import UserRole

router = Router(name="common")


@router.message(
    Command("cancel"),
    RoleFilter(role=[UserRole.USER, UserRole.ADMIN]),
)
async def cancel_handler(message: Message, **kwargs) -> None:
    await message.answer(text="Use /add_channel <url> [label] to add channel.")


__all__ = ["router"]
