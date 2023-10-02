import operator
import time
from datetime import datetime
from typing import Optional

import aiofiles
import aiogram
import structlog
import yt_dlp
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNetworkError
from sulguk import SULGUK_PARSE_MODE

from .schemas import ChannelDescription
from src.config import Channel
from src.decorators import wrap_sync_to_async

logger = structlog.stdlib.get_logger()


def make_readable(seconds):
    h = seconds // 3600
    m = (seconds - h * 3600) // 60
    s = seconds - (h * 3600) - (m * 60)
    return f"{h:0>2d}:{m:0>2d}:{s:0>2d}"


def check_live_streams(
    channels: list[Channel], ydl: yt_dlp.YoutubeDL
) -> list[ChannelDescription]:
    """
    :param channels:
    :return:
    """
    result: list[ChannelDescription] = []

    for channel in channels:
        logger.info(channel)
        time.sleep(1)
        try:
            # Get basic streams info from YT
            streams_info = ydl.extract_info(
                url=f"{channel.url}/streams",
                download=False,
                process=False,
                force_generic_extractor=False,
            )
            # get all stream entries
            entries = streams_info.get("entries", None)
            if entries is not None:
                for entry in entries:
                    if entry["live_status"] == "is_live":
                        try:
                            logger.info(f"Live {channel.label} {channel.url}")

                            live_info = ydl.extract_info(
                                url=entry["url"],
                                download=False,
                                process=False,
                                force_generic_extractor=False,
                            )

                            concurrent_view_count = live_info.get(
                                "concurrent_view_count", 0
                            )
                            like_count = live_info.get("like_count", 0)
                            release_timestamp = live_info["release_timestamp"]
                            duration = make_readable(
                                int(datetime.now().timestamp() - release_timestamp)
                            )
                            url = live_info["original_url"]

                            result.append(
                                ChannelDescription(
                                    url=url,
                                    label=channel.label,
                                    like_count=like_count,
                                    concurrent_view_count=concurrent_view_count,
                                    duration=duration,
                                )
                            )

                            break
                        except Exception as ex:
                            logger.error(f"inner {channel.url} {ex}")

        except Exception as ex:
            logger.error(f"outer {channel.url} {ex}")

    result = sorted(
        result, key=operator.attrgetter("concurrent_view_count"), reverse=True
    )
    return result


async_check_live_streams = wrap_sync_to_async(check_live_streams)


async def check_if_need_send_instead_of_edit(
    bot: Bot,
    message_id: Optional[int],
    from_chat_id: int,
    delta: int = 3,
) -> bool:
    if not message_id:
        return True

    deep: int = 20

    result = []

    for i in range(1, deep, 1):
        try:
            message_id_to_check = message_id + i
            await bot.copy_message(
                chat_id=773542466,
                from_chat_id=from_chat_id,
                message_id=message_id_to_check,
                disable_notification=True,
                allow_sending_without_reply=True,
            )
            result.append(1)
        except aiogram.exceptions.TelegramBadRequest as ex:
            await logger.ainfo(f"{ex}")
            result.append(0)

    if sum(result) >= delta:
        return True
    else:
        return False


async def send_report(
    bot: Bot,
    channels: list[Channel],
    chat_id: str,
    ydl: yt_dlp.YoutubeDL,
):
    """
    :param ydl:
    :param bot:
    :param channels:
    :param chat_id:
    :return:
    """

    live_list: list[ChannelDescription] = await async_check_live_streams(
        channels=channels, ydl=ydl
    )

    await logger.ainfo(f"Live list length {len(live_list)}")

    msg_header = f"""
    <h1>✅ СЕЙЧАС В ЭФИРЕ:</h1>
    <br/>
    """
    msg_footer = f"""
    <hr/>
    <i>Powered by <a href='https://t.me/diskordovoselo'>DiskordovoSelo</a></i>
    """

    msg_body = ""

    if live_list:
        msg_body += "<ol type='1'>"
        for cd in live_list:
            entry_body = ""

            entry_body += f"<b><a href='{cd.url}'>{cd.label}</a></b> <br/>"
            if cd.concurrent_view_count:
                entry_body += f"<b>👀 Cмотрят: {cd.concurrent_view_count}</b> <br/>"

            if cd.like_count:
                entry_body += f"<b>👍 Понравилось: {cd.like_count}</b> <br/>"

            if cd.duration:
                entry_body += f"<b>🕑 Длительность: {cd.duration}</b> <br/>"

            entry_body = "<li>" + entry_body + "</li>"
            entry_body += "<br/>"

            msg_body += entry_body

        msg_body += "</ol>"

    await logger.ainfo(f"Body: {msg_body}")

    if msg_body:
        message_text = msg_header + msg_body + msg_footer

        message_id = await pull_message_id()
        if message_id is not None:
            try:
                is_needed_send = await check_if_need_send_instead_of_edit(
                    message_id=message_id, delta=3, bot=bot, from_chat_id=int(chat_id)
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


async def pull_message_id(filepath: str = "messages.dump") -> Optional[int]:
    message_id: Optional[int] = None
    try:
        async with aiofiles.open(file=filepath, mode="r") as fh:
            message_id = int(await fh.readline())
    except Exception as ex:
        await logger.aerror(f"Pull: {ex}")

    return message_id


async def push_message_id(message_id: int, filepath: str = "messages.dump") -> int:
    try:
        async with aiofiles.open(file=filepath, mode="w") as fh:
            await fh.write(str(message_id))
    except Exception as ex:
        await logger.aerror(f"Push: {ex}")

    return message_id


__all__ = ["send_report"]
