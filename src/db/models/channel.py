from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from .mixins import ModelORM
from .mixins import RepresentationMixin
from .mixins import TimestampsMixin
from .user import UserORMRelatedModel


class ChannelORM(ModelORM, TimestampsMixin, UserORMRelatedModel, RepresentationMixin):
    """
    Model for storing YT channels
    """

    __tablename__ = "channels"

    __table_args__ = (UniqueConstraint("url", name="ix_uniq_url"),)
    # some features with autoincrement
    # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#allowing-autoincrement-behavior-sqlalchemy-types-other-than-integer-integer
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    url = Column(String(length=255), nullable=False, index=True)
    label = Column(String(length=255), nullable=False, index=True)
    enabled = Column(Boolean, default=True, index=True)
    user = relationship(
        "UserORM",
        backref="channels",
        foreign_keys="ChannelORM.user_id",
        uselist=False,
        lazy="selectin",
    )


class ChannelORMRelatedModel:
    __abstract__ = True

    channel_id = Column(
        ForeignKey(
            f"{ChannelORM.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )


__all__ = ["ChannelORM", "ChannelORMRelatedModel"]
