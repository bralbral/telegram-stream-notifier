from datetime import datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlmodel import Field
from sqlmodel import SQLModel


class MessageLogModel(SQLModel, table=True):

    __tablename__ = "message_logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        )
    )
    message_id: int = Field(index=True)
    text: str = Field(nullable=False, index=False)


__all__ = ["MessageLogModel"]
