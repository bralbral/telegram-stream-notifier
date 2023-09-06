from typing import Optional

from pydantic import BaseModel


class ChannelDescription(BaseModel):
    url: str
    label: str
    concurrent_view_count: Optional[int] = None


__all__ = ["ChannelDescription"]
