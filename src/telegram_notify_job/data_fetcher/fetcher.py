import asyncio
import operator
from datetime import datetime
from typing import Optional

import structlog
import yt_dlp

from ...schemas import ChannelSchema
from ..schemas import ChannelDescription
from .utils import make_time_readable
from src.decorators import wrap_sync_to_async

logger = structlog.stdlib.get_logger()


def fetch_live_stream(
    channel: ChannelSchema, ydl: yt_dlp.YoutubeDL
) -> Optional[ChannelDescription]:
    """
    :param ydl:
    :param channel:
    :return:
    """
    logger.info(channel.model_dump_json())

    live_stream = None

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
                        duration = make_time_readable(
                            int(datetime.now().timestamp() - release_timestamp)
                        )
                        url = live_info["original_url"]
                        live_stream = ChannelDescription(
                            url=url,
                            label=channel.label,
                            like_count=like_count,
                            concurrent_view_count=concurrent_view_count,
                            duration=duration,
                        )
                        break

                    except Exception as ex:
                        logger.error(f"inner {channel.url} {ex}")
                        break

    except Exception as ex:
        logger.error(f"outer {channel.url} {ex}")

    return live_stream


async_fetch_livestream = wrap_sync_to_async(fetch_live_stream)


async def async_fetch_livestreams(
    channels: list[ChannelSchema], ydl: yt_dlp.YoutubeDL
) -> list[ChannelDescription]:
    """
    :param ydl:
    :param channels:
    :return:
    """
    tasks = [async_fetch_livestream(channel=channel, ydl=ydl) for channel in channels]

    live_streams = await asyncio.gather(*tasks)
    live_streams = [
        stream for stream in live_streams if isinstance(stream, ChannelDescription)
    ]
    live_streams = sorted(
        live_streams, key=operator.attrgetter("concurrent_view_count"), reverse=True
    )
    return live_streams


__all__ = ["async_fetch_livestreams"]
