from datetime import datetime
from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel


class BaseSQLModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


__all__ = ["BaseSQLModel"]
