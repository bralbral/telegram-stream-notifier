from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State
from aiogram.types import Message

from ..filters import RoleFilter
from ..filters import UserRole

router = Router(name="admins")


@router.message(
    Command("channels"),
    RoleFilter(role=[UserRole.ADMIN, UserRole.SUPERUSER]),
    State(state="*"),
)
async def start_channels_dialog(message: Message, **kwargs):
    await message.answer("Started.")


__all__ = ["router"]
