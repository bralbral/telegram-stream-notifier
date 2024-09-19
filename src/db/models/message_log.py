from sqlmodel import Field

from .base import BaseModel


class MessageLogModel(BaseModel, table=True):

    __tablename__ = "message_logs"

    message_id: int = Field(index=True)
    text: str = Field(nullable=False, index=False)


__all__ = ["MessageLogModel"]
