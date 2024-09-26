from typing import Optional

import yt_dlp
from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNetworkError
from aiogram.utils.chat_action import ChatActionSender
from sulguk import SULGUK_PARSE_MODE
from twitchAPI.twitch import Twitch

from ..data_fetcher import async_twitch_fetch_livestreams
from ..data_fetcher import async_youtube_fetch_livestreams
from ..dto import ErrorVideoInfo
from ..dto import VideoInfo
from ..report_generator import generate_jinja_report
from .utils import check_if_need_send_instead_of_edit
from src.db import DataAccessLayer
from src.db.models import MessageLogModel
from src.db.models.channel_type import ChannelType
from src.logger import logger


async def notify(
    bot: Bot,
    chat_id: int,
    temp_chat_id: int,
    ydl: yt_dlp.YoutubeDL,
    empty_template: Optional[str],
    report_template: str,
    dal: DataAccessLayer,
    twitch: Optional[Twitch] = None,
) -> None:
    """
    :param dal:
    :param report_template:
    :param empty_template:
    :param temp_chat_id:
    :param ydl:
    :param bot:
    :param chat_id:
    :param twitch
    :return:
    """

    # get channels
    channels = await dal.get_channels(enabled=True)

    youtube_channels = [
        channel for channel in channels if channel.type.type == ChannelType.YOUTUBE
    ]
    twitch_channels = [
        channel for channel in channels if channel.type.type == ChannelType.TWITCH
    ]

    data: tuple[list[VideoInfo], list[ErrorVideoInfo]] = (
        await async_youtube_fetch_livestreams(channels=youtube_channels, ydl=ydl)
    )

    live_list, errors = data

    if twitch:
        _twitch = await twitch

        twitch_data: tuple[list[VideoInfo], list[ErrorVideoInfo]] = (
            await async_twitch_fetch_livestreams(
                channels=twitch_channels, twitch=_twitch
            )
        )

        twitch_live_list, twitch_errors = twitch_data
        live_list.extend(twitch_live_list)
        errors.extend(twitch_errors)

    # logging errors
    for error in errors:
        await logger.aerror(f"Error with {error.channel['id']}: {error.ex_message}")

    await logger.ainfo(f"Live list length {len(live_list)}")

    message_text: Optional[str] = generate_jinja_report(
        data=live_list, report_template=report_template, empty_template=empty_template
    )

    if message_text:
        message_id: Optional[int] = await dal.get_last_published_message_id()

        if message_id is not None:
            try:
                async with ChatActionSender(
                    bot=bot, chat_id=chat_id, action=ChatAction.TYPING
                ):
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
                            await bot.delete_message(
                                chat_id=chat_id, message_id=message_id
                            )
                        except TelegramBadRequest as ex:
                            await logger.aerror(
                                f"Msg: {message_id} cannot be deleted {ex}"
                            )

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
                        "specified new message content and reply markup are exactly the same as a current"
                        " content and reply markup of the message"
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
            await dal.create_message(
                obj=MessageLogModel(message_id=message_id, text=message_text)
            )


__all__ = ["notify"]
