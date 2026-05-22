from .base import DTO


class ErrorVideoInfo(DTO):
    channel: dict
    ex_message: str


class VideoInfo(DTO):
    url: str
    label: str
    channel: dict | None = None
    concurrent_view_count: int | None = None
    duration: str | None = None
    like_count: int | None = None


__all__ = ["ErrorVideoInfo", "VideoInfo"]
