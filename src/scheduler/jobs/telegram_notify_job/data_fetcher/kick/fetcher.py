import asyncio
import operator
from datetime import datetime
from typing import Optional

from aiohttp import ClientSession
from dateutil.tz import tzutc

from .constants import KICK_API_URL
from src.db.models import ChannelModel
from src.logger import logger
from src.scheduler.jobs.telegram_notify_job.data_fetcher.utils import make_time_readable
from src.scheduler.jobs.telegram_notify_job.dto import ErrorVideoInfo
from src.scheduler.jobs.telegram_notify_job.dto import VideoInfo
from src.utils import extract_kick_username


async def async_fetch_livestream(
    channel: ChannelModel, session: ClientSession
) -> Optional[VideoInfo] | ErrorVideoInfo:
    """
    :param session:
    :param channel:
    :return:
    """
    await logger.ainfo(channel.model_dump_json())

    live_stream = None
    try:

        username = extract_kick_username(channel.url)
        if not username:
            raise Exception(f"Cannot extract username for {channel.url}")

        async with session.get(f"{KICK_API_URL}{username}") as resp:

            raw_data = await resp.json()

            livestream: Optional[dict] = raw_data.get("livestream", None)
            if livestream:
                is_live = livestream.get("is_live", None)

                if is_live:

                    concurrent_view_count = livestream["viewer_count"]

                    duration = make_time_readable(
                        (
                            datetime.now(tz=tzutc())
                            - datetime.strptime(
                                livestream["start_time"], "%Y-%m-%d %H:%M:%S"
                            )
                        ).seconds
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


async def async_kick_fetch_livestreams(
    channels: list[ChannelModel],
) -> tuple[list[VideoInfo], list[ErrorVideoInfo]]:
    """
    :param channels:
    :return:
    """

    async with ClientSession() as client:
        tasks = [
            async_fetch_livestream(channel=channel, session=client)
            for channel in channels
        ]

        data = await asyncio.gather(*tasks)

    errors = [stream for stream in data if isinstance(stream, ErrorVideoInfo)]

    live_streams = [stream for stream in data if isinstance(stream, VideoInfo)]

    live_streams = sorted(
        live_streams, key=operator.attrgetter("concurrent_view_count"), reverse=True
    )

    return live_streams, errors


__all__ = ["async_kick_fetch_livestreams"]
