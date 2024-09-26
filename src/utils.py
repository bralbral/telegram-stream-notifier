import re
from typing import Optional

YOUTUBE_USERNAME_CHANNEL_LINK_PATTERN = re.compile(
    r"^https?://(?:www\.)?youtube\.com/@[\w-]+/?$"
)

TWITCH_USERNAME_CHANNEL_LINK_PATTERN = re.compile(
    r"^https?://(?:www\.)?twitch\.tv/([\w-]+)/?$"
)


def youtube_channel_url_validator(link: str) -> bool:
    match = re.match(YOUTUBE_USERNAME_CHANNEL_LINK_PATTERN, link)
    return bool(match)


def twitch_channel_url_validator(link: str) -> bool:
    match = re.match(TWITCH_USERNAME_CHANNEL_LINK_PATTERN, link)
    return bool(match)


def extract_twitch_username(link: str) -> Optional[str]:
    match = re.match(TWITCH_USERNAME_CHANNEL_LINK_PATTERN, link)
    if match:
        return match.group(1)
    return None


def kick_channel_url_validator(link: str) -> bool:
    return False


__all__ = [
    "extract_twitch_username",
    "kick_channel_url_validator",
    "twitch_channel_url_validator",
    "youtube_channel_url_validator",
]
