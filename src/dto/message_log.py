from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from pydantic import Field

from .base import DTO


class MessageLogDTO(DTO):
    id: Optional[int] = None
    message_id: int
    text: str
    updated_at: datetime = Field(default=datetime.utcnow())

    model_config = ConfigDict(from_attributes=True)


__all__ = ["MessageLogDTO"]
