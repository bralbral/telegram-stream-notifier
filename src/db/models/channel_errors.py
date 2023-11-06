from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint

from .channel import ChannelOrmRelatedModel
from .mixins import CounterMixin
from .mixins import ModelOrm
from .mixins import RepresentationMixin
from .mixins import TimestampsMixin


class ChannelErrorOrm(
    ModelOrm, TimestampsMixin, CounterMixin, ChannelOrmRelatedModel, RepresentationMixin
):
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


__all__ = ["ChannelErrorOrm"]
