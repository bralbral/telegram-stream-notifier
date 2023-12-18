import re

YOUTUBE_USERNAME_CHANNEL_LINK_PATTERN = re.compile(
    r"^https?://(?:www\.)?youtube\.com/@[\w-]+/?$"
)


def youtube_channel_url_validator(link: str):
    match = re.match(YOUTUBE_USERNAME_CHANNEL_LINK_PATTERN, link)
    return bool(match)


__all__ = ["youtube_channel_url_validator"]
