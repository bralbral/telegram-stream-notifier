from datetime import datetime

from pydantic import ConfigDict
from pydantic import Field

from .base import DTO


class MessageLogBaseDTO(DTO):
    message_id: int
    text: str
    updated_at: datetime = Field(default=datetime.utcnow())

    model_config = ConfigDict(from_attributes=True)


class MessageLogCreateDTO(MessageLogBaseDTO):
    ...


class MessageLogRetrieveDTO(MessageLogCreateDTO):
    id: int


__all__ = ["MessageLogCreateDTO", "MessageLogRetrieveDTO"]
