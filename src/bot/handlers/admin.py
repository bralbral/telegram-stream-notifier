from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import State
from aiogram.types import Message

from ...db import DataAccessLayer
from ...schemas import ChannelSchema
from ..filters import RoleFilter
from ..filters import UserRole

router = Router(name="admins")


@router.message(
    Command("channels"),
    RoleFilter(role=[UserRole.ADMIN, UserRole.SUPERUSER]),
    State(state="*"),
)
async def start_channels_dialog(message: Message, **kwargs):
    dal: DataAccessLayer = kwargs["dal"]

    user_schema = await dal.get_user_by_attr(**{"user_id": message.from_user.id})
    if user_schema:
        channel_schema = ChannelSchema(
            url="https://www.youtube.com/@SLOVOproject",
            label="slovo",
            enabled=True,
            user_id=user_schema.user_id,
        )

        result = await dal.create_channel(channel_schema=channel_schema)

    await message.answer("Started.")


__all__ = ["router"]
