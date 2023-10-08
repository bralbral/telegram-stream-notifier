from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint

from .channel import ChannelOrmRelatedModel
from src.db.mixins import Base
from src.db.mixins import CounterMixin
from src.db.mixins import TimestampsMixin


class ChannelErrorOrm(Base, TimestampsMixin, CounterMixin, ChannelOrmRelatedModel):
    """
    Base
    """

    __tablename__ = "channel_errors"

    __table_args__ = (UniqueConstraint("channel_id", name="ix_uniq_channel_id"),)
    # some features with autoincrement
    # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#allowing-autoincrement-behavior-sqlalchemy-types-other-than-integer-integer
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<id={self.id}"


__all__ = ["ChannelErrorOrm"]
