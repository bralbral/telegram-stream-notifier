from typing import Optional

from pydantic import BaseModel


class ChannelDescription(BaseModel):
    url: str
    label: str
    like_count: Optional[int] = None
    concurrent_view_count: Optional[int] = None
    duration: Optional[str] = None


__all__ = ["ChannelDescription"]
