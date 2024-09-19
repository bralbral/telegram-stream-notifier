from typing import Optional

from .base import DTO


class TwitchVideoInfoDTO(DTO):
    url: str
    label: str
    concurrent_view_count: Optional[int] = None
    duration: Optional[str] = None


class TwitchErrorInfoDTO(DTO):
    channel: str
    ex_message: str


__all__ = ["TwitchErrorInfoDTO", "TwitchVideoInfoDTO"]
