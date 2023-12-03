import re

YOUTUBE_USERNAME_CHANNEL_LINK_PATTERN = re.compile(r"https://www\.youtube\.com/@(\w+)")


def url_validator(link: str):
    match = re.match(YOUTUBE_USERNAME_CHANNEL_LINK_PATTERN, link)
    return bool(match)


__all__ = ["url_validator"]
