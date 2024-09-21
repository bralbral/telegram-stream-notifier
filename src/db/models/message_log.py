from sqlmodel import Field

from .base import BaseSQLModel


class MessageLogModel(BaseSQLModel):

    __tablename__ = "message_logs"

    message_id: int = Field(index=True)
    text: str = Field(nullable=False, index=False)


__all__ = ["MessageLogModel"]
