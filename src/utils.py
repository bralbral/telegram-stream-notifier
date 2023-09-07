import operator
from datetime import datetime
from typing import Any
from typing import Optional

import aiofiles
import yt_dlp
from aiogram import Bot
from sulguk import SULGUK_PARSE_MODE

from src.channel_description import ChannelDescription
from src.decorators import wrap_sync_to_async
from src.logger import logger


def make_readable(seconds):
    h = seconds // 3600
    m = (seconds - h * 3600) // 60
    s = seconds - (h * 3600) - (m * 60)
    return f"{h:0>2d}:{m:0>2d}:{s:0>2d}"


def check_live_streams(
    channel_descriptions: list[ChannelDescription],
) -> list[ChannelDescription]:
    """
    :param channel_descriptions:
    :return:
    """
    result: list[ChannelDescription] = []

    ydl_opts: dict[str, Any] = {"quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_d in channel_descriptions:
            logger.info(f"{channel_d.label} {channel_d.url} started")
            try:
                # Get basic streams info from YT
                streams_info = ydl.extract_info(
                    url=f"{channel_d.url}/streams",
                    download=False,
                    process=False,
                    force_generic_extractor=False,
                )
                logger.info(f"{channel_d.label} {channel_d.url} stream_info")
                # get all stream entries
                entries = streams_info.get("entries", None)
                if entries:
                    for entry in entries:
                        # get info for using entry url
                        if entry["live_status"] == "is_live":
                            logger.info(f"{channel_d.label} {channel_d.url} live")
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

                            channel_d.concurrent_view_count = (
                                concurrent_view_count
                                if concurrent_view_count is not None
                                else 0
                            )
                            channel_d.url = url
                            channel_d.like_count = like_count
                            channel_d.duration = duration

                            result.append(channel_d)
                            logger.info(f"{channel_d.label} {channel_d.url} finished")
                            break
                else:
                    logger.error(f"Entries from {channel_d.url}/streams is empty")

            except Exception as ex:
                logger.error(f"{channel_d.url} {ex}")

    logger.info(f"Sort results")
    result = sorted(
        result, key=operator.attrgetter("concurrent_view_count"), reverse=True
    )
    return result


async_check_live_streams = wrap_sync_to_async(check_live_streams)


async def send_report(
    bot: Bot, channel_descriptions: list[ChannelDescription], chat_id: str
):
    """
    :param bot:
    :param channel_descriptions:
    :param chat_id:
    :return:
    """
    live_list: list[ChannelDescription] = await async_check_live_streams(
        channel_descriptions=channel_descriptions
    )

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

    if msg_body:
        message_text = msg_header + msg_body + msg_footer

        message_id = await pull_message_id()

        try:
            msg = await bot.edit_message_text(
                chat_id=chat_id,
                text=message_text,
                message_id=message_id,
                parse_mode=SULGUK_PARSE_MODE,
                disable_web_page_preview=True,
            )

            message_id = msg.message_id

            await logger.ainfo(f"Msg: { message_id} edited")

        except Exception as ex:
            await logger.aerror(f"Editing: {ex}")

            msg = await bot.send_message(
                text=message_text,
                chat_id=chat_id,
                parse_mode=SULGUK_PARSE_MODE,
                disable_web_page_preview=True,
            )

            message_id = msg.message_id

            await logger.ainfo(f"Msg: { message_id} sent")

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
