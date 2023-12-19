from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from ..filters import RoleFilter
from ..filters import UserRole

router = Router(name="common")


@router.message(
    Command("cancel"),
    RoleFilter(role=[UserRole.USER, UserRole.SUPERUSER]),
    State(state="*"),
)
async def cancel_handler(message: Message, state: FSMContext, **kwargs) -> None:
    await message.answer(text="States cleared.", reply_markup=ReplyKeyboardRemove())
    await state.clear()


__all__ = ["router"]
