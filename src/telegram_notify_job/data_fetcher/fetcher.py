import operator
import time
from datetime import datetime

import structlog
import yt_dlp

from ..schemas import ChannelDescription
from .utils import make_time_readable
from src.config import Channel
from src.decorators import wrap_sync_to_async

logger = structlog.stdlib.get_logger()


def fetch_live_streams(
    channels: list[Channel], ydl: yt_dlp.YoutubeDL
) -> list[ChannelDescription]:
    """
    :param ydl:
    :param channels:
    :return:
    """
    result: list[ChannelDescription] = []

    for channel in channels:
        logger.info(channel.model_dump_json())
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

                            # # Try to get paused streams
                            # upload_date = live_info.get("upload_date", None)
                            # if upload_date:
                            #     logger.info(
                            #         f"Pause or stuck {channel.label} {channel.url}"
                            #     )
                            #     break

                            concurrent_view_count = live_info.get(
                                "concurrent_view_count", 0
                            )
                            like_count = live_info.get("like_count", 0)
                            release_timestamp = live_info["release_timestamp"]
                            duration = make_time_readable(
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


async_fetch_livestreams = wrap_sync_to_async(fetch_live_streams)


__all__ = ["async_fetch_livestreams"]
