import yt_dlp
from aiogram import Bot
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramBadRequest
from aiogram.exceptions import TelegramNetworkError
from aiogram.utils.chat_action import ChatActionSender
from sulguk import SULGUK_PARSE_MODE
from twitchAPI.twitch import Twitch

from ..data_fetcher import async_kick_fetch_livestreams
from ..data_fetcher import async_twitch_fetch_livestreams
from ..data_fetcher import async_youtube_fetch_livestreams
from ..dto import ErrorVideoInfo
from ..dto import VideoInfo
from ..report_generator import generate_jinja_report
from src.db import DataAccessLayer
from src.db.models.channel_type import ChannelType
from src.logger import logger


async def notify(
    bot: Bot,
    chat_id: int,
    temp_chat_id: int,
    ydl: yt_dlp.YoutubeDL,
    empty_template: str | None,
    report_template: str,
    dal: DataAccessLayer,
    twitch: Twitch | None = None,
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

    # get channels with subscribers
    channels = await dal.get_channels(enabled=True)

    if channels:
        youtube_channels = [
            channel for channel in channels if channel.type.type == ChannelType.YOUTUBE
        ]
        twitch_channels = [
            channel for channel in channels if channel.type.type == ChannelType.TWITCH
        ]
        kick_channels = [
            channel for channel in channels if channel.type.type == ChannelType.KICK
        ]

        data: tuple[
            list[VideoInfo], list[ErrorVideoInfo]
        ] = await async_youtube_fetch_livestreams(channels=youtube_channels, ydl=ydl)

        live_list, errors = data

        if twitch and twitch_channels:
            _twitch = await twitch

            twitch_data: tuple[
                list[VideoInfo], list[ErrorVideoInfo]
            ] = await async_twitch_fetch_livestreams(
                channels=twitch_channels, twitch=_twitch
            )

            twitch_live_list, twitch_errors = twitch_data
            live_list.extend(twitch_live_list)
            errors.extend(twitch_errors)

        if kick_channels:
            kick_data: tuple[
                list[VideoInfo], list[ErrorVideoInfo]
            ] = await async_kick_fetch_livestreams(channels=kick_channels)

            kick_live_list, kick_errors = kick_data
            live_list.extend(kick_live_list)
            errors.extend(kick_errors)

        # logging errors
        for error in errors:
            await logger.aerror(f"Error with {error.channel['id']}: {error.ex_message}")

        await logger.ainfo(f"Live list length {len(live_list)}")

        message_text: str | None = generate_jinja_report(
            data=live_list,
            report_template=report_template,
            empty_template=empty_template,
        )

        if message_text:
            # Group live streams by channel and notify subscribers
            channels_to_notify: dict[int, list[VideoInfo]] = {}
            for video in live_list:
                if video.channel:
                    channel_id = video.channel.get("id")
                    if channel_id:
                        if channel_id not in channels_to_notify:
                            channels_to_notify[channel_id] = []
                        channels_to_notify[channel_id].append(video)

            for channel in channels:
                channel_videos = channels_to_notify.get(channel.id, [])
                if channel_videos:
                    # Get all subscribers for this channel
                    subscribers = await channel.subscribers.all()
                    for subscriber in subscribers:
                        try:
                            async with ChatActionSender(
                                bot=bot,
                                chat_id=subscriber.user_id,
                                action=ChatAction.TYPING,
                            ):
                                msg = await bot.send_message(
                                    text=message_text,
                                    chat_id=subscriber.user_id,
                                    parse_mode=SULGUK_PARSE_MODE,
                                    disable_web_page_preview=True,
                                )
                                await logger.ainfo(
                                    f"Msg: {msg.message_id} sent to user {subscriber.user_id}"
                                )
                        except TelegramNetworkError as ex:
                            await logger.aerror(
                                f"Exc: TelegramNetworkError for user {subscriber.user_id}: {ex}"
                            )
                        except TelegramBadRequest as ex:
                            await logger.aerror(
                                f"Error sending message to user {subscriber.user_id}: {ex}"
                            )


__all__ = ["notify"]
