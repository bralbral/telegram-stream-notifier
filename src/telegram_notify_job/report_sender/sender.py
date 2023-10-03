from typing import Optional

import structlog
import yt_dlp
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNetworkError
from sulguk import SULGUK_PARSE_MODE

from ..data_fetcher import async_fetch_livestreams
from ..report_generator import generate_report
from ..schemas import ChannelDescription
from .utils import check_if_need_send_instead_of_edit
from .utils import pull_message_id
from .utils import push_message_id
from src.config import Channel

logger = structlog.stdlib.get_logger()


async def send_report(
    bot: Bot,
    channels: list[Channel],
    chat_id: int,
    temp_chat_id: int,
    ydl: yt_dlp.YoutubeDL,
) -> None:
    """
    :param temp_chat_id:
    :param ydl:
    :param bot:
    :param channels:
    :param chat_id:
    :return:
    """

    live_list: list[ChannelDescription] = await async_fetch_livestreams(
        channels=channels, ydl=ydl
    )
    await logger.ainfo(f"Live list length {len(live_list)}")

    message_text: Optional[str] = generate_report(data=live_list)

    if message_text:
        message_id = await pull_message_id()
        if message_id is not None:
            try:
                is_needed_send = await check_if_need_send_instead_of_edit(
                    message_id=message_id,
                    delta_messages=3,
                    bot=bot,
                    from_chat_id=chat_id,
                    to_chat_id=temp_chat_id,
                )

                if not is_needed_send:
                    msg = await bot.edit_message_text(
                        chat_id=chat_id,
                        text=message_text,
                        message_id=message_id,
                        parse_mode=SULGUK_PARSE_MODE,
                        disable_web_page_preview=True,
                    )
                    message_id = msg.message_id
                    await logger.ainfo(f"Msg: {message_id} edited")
                else:
                    try:
                        await bot.delete_message(chat_id=chat_id, message_id=message_id)
                    except TelegramBadRequest as ex:
                        await logger.aerror(f"Msg: {message_id} cannot be deleted {ex}")

                    msg = await bot.send_message(
                        text=message_text,
                        chat_id=chat_id,
                        parse_mode=SULGUK_PARSE_MODE,
                        disable_web_page_preview=True,
                    )

                    message_id = msg.message_id

                    await logger.ainfo(f"Msg: {message_id} sent")

            except TelegramNetworkError as ex:
                await logger.aerror(f"Exc: TelegramNetworkError finish cycle: {ex}")
                return

            except TelegramBadRequest as ex:
                if (
                    str(ex).find(
                        "specified new message content and reply markup are exactly the same as a current content and reply markup of the message"
                    )
                    > -1
                ):
                    await logger.aerror(f"Same message: {ex}")
                else:
                    await logger.aerror(f"Editing: {ex}")

                    msg = await bot.send_message(
                        text=message_text,
                        chat_id=chat_id,
                        parse_mode=SULGUK_PARSE_MODE,
                        disable_web_page_preview=True,
                    )

                    message_id = msg.message_id

                    await logger.ainfo(f"Msg: {message_id} sent")

        else:
            await logger.ainfo(f"Message_id is None, sending")

            msg = await bot.send_message(
                text=message_text,
                chat_id=chat_id,
                parse_mode=SULGUK_PARSE_MODE,
                disable_web_page_preview=True,
            )

            message_id = msg.message_id

            await logger.ainfo(f"Msg: {message_id} sent")

        if message_id:
            await push_message_id(message_id=message_id)


__all__ = ["send_report"]
