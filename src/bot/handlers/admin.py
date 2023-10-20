from urllib.parse import urlparse

from aiogram import F
from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
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
