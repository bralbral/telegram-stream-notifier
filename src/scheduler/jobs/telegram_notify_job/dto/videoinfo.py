from typing import Optional

from .base import DTO


class ErrorVideoInfo(DTO):
    channel: dict
    ex_message: str


class VideoInfo(DTO):
    url: str
    label: str
    concurrent_view_count: Optional[int] = None
    duration: Optional[str] = None
    like_count: Optional[int] = None


__all__ = ["ErrorVideoInfo", "VideoInfo"]
