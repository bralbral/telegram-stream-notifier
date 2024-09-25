from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog import StartMode

from ....db import DataAccessLayer
from ...filters import RoleFilter
from ...filters import UserRole
from ...states import ChannelCreateSG


add_channel_router = Router(name="add_channel")


@add_channel_router.message(
    Command("add_channel"),
    RoleFilter(role=[UserRole.USER, UserRole.SUPERUSER]),
    State(state="*"),
)
async def start_add_channel_dialog(
    message: Message,
    dialog_manager: DialogManager,
    dal: DataAccessLayer,
    role: UserRole,
    **kwargs,
) -> None:
    await dialog_manager.start(
        ChannelCreateSG.start,
        mode=StartMode.RESET_STACK,
        data={
            "dal": dal,
        },
    )


__all__ = ["add_channel_router"]
