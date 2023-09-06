from typing import Any
from typing import Optional

import aiofiles
import yt_dlp
from aiogram import Bot
from sulguk import SULGUK_PARSE_MODE

from src.channel_description import ChannelDescription
from src.decorators import wrap_sync_to_async
from src.logger import logger


def check_live_streams(
    channel_descriptions: list[ChannelDescription],
) -> list[ChannelDescription]:
    """
    :param channel_descriptions:
    :return:
    """
    result: list[ChannelDescription] = []

    ydl_opts: dict[str, Any] = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_d in channel_descriptions:
            try:
                # Get basic streams info from YT
                streams_info = ydl.extract_info(
                    url=f"{channel_d.url}/streams",
                    download=False,
                    process=False,
                    force_generic_extractor=False,
                )
                # get all stream entries
                for entry in streams_info["entries"]:
                    # get info for using entry url
                    if entry["live_status"] == "is_live":
                        concurrent_view_count = entry["concurrent_view_count"]
                        channel_d.concurrent_view_count = (
                            concurrent_view_count
                            if concurrent_view_count is not None
                            else 0
                        )
                        channel_d.url = entry["url"]
                        result.append(channel_d)
                        break

            except yt_dlp.utils.DownloadError as ex:
                logger.error(f"{channel_d.url} {ex}")

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
    <b>✅ СЕЙЧАС В ЭФИРЕ:<b>
    <br/>
    <br/>
    """
    msg_footer = f"""
    <br/>
    <br/>
    <b>------------------------</b>
    """

    msg_body = ""

    if live_list:
        msg_body += "<ul>"
        for cd in live_list:
            msg_body += f"<li><a href='{cd.url}'>{cd.label}</a> <b>Cмотрят: {cd.concurrent_view_count}</b></li>"

        msg_body += "</ul>"

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
