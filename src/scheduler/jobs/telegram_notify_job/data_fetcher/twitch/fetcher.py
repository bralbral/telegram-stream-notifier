import asyncio
import operator
from typing import Optional

from black import datetime
from dateutil.tz import tzutc
from twitchAPI.helper import first
from twitchAPI.object.api import Stream
from twitchAPI.twitch import Twitch

from src.db.models import ChannelModel
from src.logger import logger
from src.scheduler.jobs.telegram_notify_job.data_fetcher.utils import make_time_readable
from src.scheduler.jobs.telegram_notify_job.dto import ErrorVideoInfo
from src.scheduler.jobs.telegram_notify_job.dto import VideoInfo


async def async_fetch_livestream(
    channel: ChannelModel, twitch: Twitch
) -> Optional[VideoInfo] | ErrorVideoInfo:
    """
    :param twitch:
    :param channel:
    :return:
    """
    await logger.ainfo(channel.model_dump_json())

    live_stream = None
    try:
        data: Optional[Stream] = await first(
            twitch.get_streams(user_login=[channel.url], first=1, stream_type="live")
        )

        if data:
            concurrent_view_count = data.viewer_count
            duration = make_time_readable(
                (datetime.now(tz=tzutc()) - data.started_at).seconds
            )

            live_stream = VideoInfo(
                url=channel.url,
                label=channel.label,
                concurrent_view_count=concurrent_view_count,
                duration=duration,
            )

    except Exception as ex:
        await logger.aerror(f"Fetching info error: {channel.url} {ex}")
        return ErrorVideoInfo(channel=channel.model_dump(), ex_message=str(ex))

    return live_stream


async def async_twitch_fetch_livestreams(
    channels: list[ChannelModel], twitch: Twitch
) -> tuple[list[VideoInfo], list[ErrorVideoInfo]]:
    """
    :param twitch:
    :param channels:
    :return:
    """
    tasks = [
        async_fetch_livestream(channel=channel, twitch=twitch) for channel in channels
    ]

    data = await asyncio.gather(*tasks)

    errors = [stream for stream in data if isinstance(stream, ErrorVideoInfo)]

    live_streams = [stream for stream in data if isinstance(stream, VideoInfo)]

    live_streams = sorted(
        live_streams, key=operator.attrgetter("concurrent_view_count"), reverse=True
    )

    return live_streams, errors


__all__ = ["async_twitch_fetch_livestreams"]
