from io import TextIOWrapper
from typing import BinaryIO
from typing import Optional

from aiogram import Bot
from aiogram import F
from aiogram import Router
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import File
from aiogram.types import Message
from sulguk import SULGUK_PARSE_MODE

from ....db import DataAccessLayer
from ....db.models import ChannelModel
from ...filters import RoleFilter
from ...filters import UserRole
from ...states import ChannelsSG
from src.utils import youtube_channel_url_validator

add_channels_router = Router(name="add_channels")


@add_channels_router.message(
    Command("add_channels"),
    RoleFilter(role=[UserRole.SUPERUSER]),
    State(state="*"),
)
async def add_channels(message: Message, state: FSMContext, **kwargs) -> None:
    await message.answer(
        text="Upload a file with format: <br/>"
        "<code>url[TAB]label[END_ROW]</code><br/>"
        "every single line == channel to insert.<br/>"
        "Set channel url in format: <b>https://www.youtube.com/@username</b>"
        "Enter /cancel for exit <br/>",
        parse_mode=SULGUK_PARSE_MODE,
    )
    await state.set_state(ChannelsSG.bulk_channels)


@add_channels_router.message(
    F.content_type == ContentType.DOCUMENT,
    RoleFilter(role=[UserRole.SUPERUSER]),
    StateFilter(ChannelsSG.bulk_channels),
)
async def channel_file_handler(
    message: Message, state: FSMContext, bot: Bot, dal: DataAccessLayer, **kwargs
) -> None:
    file_id = message.document.file_id
    file: File = await bot.get_file(file_id=file_id)

    if file.file_size >= 10 * 1024 * 1024:
        await message.answer(
            text="File too big. Try again with filesize lower then 10 mb.",
            parse_mode=SULGUK_PARSE_MODE,
        )
        return

    user = await dal.get_user_by_attr(**{"user_id": message.from_user.id})
    if user:
        _: BinaryIO = await bot.download_file(file.file_path)
        channels: list[ChannelModel] = []
        with TextIOWrapper(_, encoding="utf-8") as text_io:
            for line in text_io:
                line = line.strip()
                splitted_line = line.split("\t")
                if len(splitted_line) != 2:
                    await message.answer(
                        text=f"Malformed line {line[0:255]}. ",
                        parse_mode=SULGUK_PARSE_MODE,
                    )
                    return

                if not youtube_channel_url_validator(splitted_line[0]):
                    await message.answer(
                        text=f"Error url validation: {splitted_line[0]} <br/>"
                        "Set channel url in format: <b>https://www.youtube.com/@username</b>",
                        parse_mode=SULGUK_PARSE_MODE,
                    )
                    return

                channel = ChannelModel(
                    url=splitted_line[0],
                    label=splitted_line[1],
                    enabled=True,
                    user=user,
                )
                channels.append(channel)

        for channel in channels:
            result: Optional[ChannelModel] = await dal.create_channel(obj=channel)
            await message.answer(f"{str(result)}")

    await state.clear()


__all__ = ["add_channels_router"]
