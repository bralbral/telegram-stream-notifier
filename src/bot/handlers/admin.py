from io import TextIOWrapper
from typing import BinaryIO
from typing import Optional
from urllib.parse import urlparse

from aiogram import Bot
from aiogram import F
from aiogram import Router
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import File
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog import StartMode
from sulguk import SULGUK_PARSE_MODE

from ...db import DataAccessLayer
from ...schemas import ChannelSchema
from ..filters import RoleFilter
from ..filters import UserRole
from ..states import ChannelDialogSG
from src.logger import logger

router = Router(name="admins")


@router.message(
    Command("add_channel"),
    RoleFilter(role=[UserRole.ADMIN, UserRole.SUPERUSER]),
    State(state="*"),
)
async def add_channel(message: Message, state: FSMContext, **kwargs) -> None:
    await message.answer(
        text="Set channel url in format: <code>https://www.youtube.com/@username</code>",
        parse_mode=SULGUK_PARSE_MODE,
    )
    await state.set_state(ChannelDialogSG.input_url)


@router.message(
    Command("add_channels"),
    RoleFilter(role=[UserRole.ADMIN, UserRole.SUPERUSER]),
    State(state="*"),
)
async def add_channels(message: Message, state: FSMContext, **kwargs) -> None:
    await message.answer(
        text="Upload a file with format: <br/>"
        "<code>url[TAB]label[END_ROW]</code><br/>"
        "every single line == channel to insert.",
        parse_mode=SULGUK_PARSE_MODE,
    )
    await state.set_state(ChannelDialogSG.bulk_channels)


@router.message(
    F.content_type == ContentType.DOCUMENT,
    RoleFilter(role=[UserRole.ADMIN, UserRole.SUPERUSER]),
    StateFilter(ChannelDialogSG.bulk_channels),
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

    user_schema = await dal.get_user_by_attr(**{"user_id": message.from_user.id})
    if user_schema:
        _: BinaryIO = await bot.download_file(file.file_path)

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

                channel = ChannelSchema(
                    url=splitted_line[0],
                    label=splitted_line[1],
                    enabled=True,
                    user_id=user_schema.user_id,
                )

                result: Optional[ChannelSchema] = await dal.create_channel(
                    channel_schema=channel
                )
                await message.answer(f"{line} {str(result)}")

    await state.clear()


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


@router.message(
    StateFilter(ChannelDialogSG.input_url),
    RoleFilter(role=[UserRole.ADMIN, UserRole.SUPERUSER]),
    F.text,
)
async def url_handler(message: Message, state: FSMContext, **kwargs) -> None:
    url = message.text.lower().strip()
    if uri_validator(url):
        await state.update_data(url=url)
        await message.answer(
            f"URL set to <b>{url}</b>, enter display name or <b>/cancel</b> for reject",
            parse_mode=SULGUK_PARSE_MODE,
        )
        await state.set_state(ChannelDialogSG.input_label)
    else:
        await message.answer(
            text="Set channel url in format: <b>https://www.youtube.com/@username</b>",
            parse_mode=SULGUK_PARSE_MODE,
        )


@router.message(
    StateFilter(ChannelDialogSG.input_label),
    RoleFilter(role=[UserRole.ADMIN, UserRole.SUPERUSER]),
    F.text,
)
async def label_handler(
    message: Message, state: FSMContext, dal: DataAccessLayer, **kwargs
) -> None:
    label = message.text.strip()
    user_data = await state.get_data()
    if user_data:
        try:
            url = user_data.get("url", None)
            if url:
                user_schema = await dal.get_user_by_attr(
                    **{"user_id": message.from_user.id}
                )
                if user_schema:
                    channel_schema = ChannelSchema(
                        url=url,
                        label=label,
                        enabled=True,
                        user_id=user_schema.user_id,
                    )

                    result = await dal.create_channel(channel_schema=channel_schema)
                    if result:
                        await message.answer(
                            f"Created. <br/> "
                            f"<code>#id: {result.id}<br/>"
                            f"label: {result.label}<br/>"
                            f"url:{result.url} </code>",
                            parse_mode=SULGUK_PARSE_MODE,
                        )
                    else:
                        await message.answer(
                            f"Cannot add channel with parameters:<br/>"
                            f"<code>label: {label}<br/>"
                            f"url:{url} </code><br/>"
                            f"Contact admins.",
                            parse_mode=SULGUK_PARSE_MODE,
                        )
        except TelegramAPIError as ex:
            await logger.aerror(ex.message)
            await message.reply(
                text=f"❌ UnknownError. Notify administrators. Thank you!"
            )
        finally:
            await state.clear()
            await message.answer("States cleared.")


@router.message(
    Command("channels"),
    RoleFilter(role=[UserRole.ADMIN, UserRole.SUPERUSER]),
    State(state="*"),
)
async def start_channels_dialog(
    message: Message, dialog_manager: DialogManager, dal: DataAccessLayer, **kwargs
):
    await dialog_manager.start(
        ChannelDialogSG.scrolling, mode=StartMode.RESET_STACK, data={"dal": dal}
    )


__all__ = ["router"]
