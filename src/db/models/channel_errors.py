from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .channel import ChannelORMRelatedModel
from .mixins import ModelORM
from .mixins import RepresentationMixin
from .mixins import TimestampsMixin


class ChannelErrorORM(
    ModelORM, TimestampsMixin, ChannelORMRelatedModel, RepresentationMixin
):
    """
    Base
    """

    __tablename__ = "channel_errors"

    # some features with autoincrement
    # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#allowing-autoincrement-behavior-sqlalchemy-types-other-than-integer-integer
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    error = Column(String(length=512), nullable=False, index=True)
    channel = relationship(
        "ChannelORM",
        backref="errors",
        foreign_keys="ChannelErrorORM.channel_id",
        uselist=False,
        lazy="selectin",
    )


__all__ = ["ChannelErrorORM"]
