from typing import Optional

from .base import DTO


class YoutubeVideoInfoDTO(DTO):
    url: str
    label: str
    like_count: Optional[int] = None
    concurrent_view_count: Optional[int] = None
    duration: Optional[str] = None


class YoutubeErrorInfoDTO(DTO):
    channel: dict
    ex_message: str


__all__ = ["YoutubeErrorInfoDTO", "YoutubeVideoInfoDTO"]
