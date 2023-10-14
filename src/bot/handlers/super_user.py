from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State
from aiogram.types import Message

from ..filters import RoleFilter
from ..filters import UserRole

router = Router(name="superusers")


@router.message(
    Command("add_admin"),
    RoleFilter(role=[UserRole.SUPERUSER]),
    State(state="*"),
)  # type: ignore
async def add_user(message: Message, **kwargs):
    await message.answer("Added.")


__all__ = ["router"]
