import re

YOUTUBE_USERNAME_CHANNEL_LINK_PATTERN = re.compile(
    r"^https?://(?:www\.)?youtube\.com/@[\w-]+/?$"
)


def youtube_channel_url_validator(link: str) -> bool:
    match = re.match(YOUTUBE_USERNAME_CHANNEL_LINK_PATTERN, link)
    return bool(match)


def twitch_channel_url_validator(link: str) -> bool:
    return False


def kick_channel_url_validator(link: str) -> bool:
    return False


__all__ = [
    "kick_channel_url_validator",
    "twitch_channel_url_validator",
    "youtube_channel_url_validator",
]
