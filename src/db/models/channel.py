from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from .mixins import ModelOrm
from .mixins import RepresentationMixin
from .mixins import TimestampsMixin
from .user import UserOrmRelatedModel


class ChannelOrm(ModelOrm, TimestampsMixin, UserOrmRelatedModel, RepresentationMixin):
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
        "UserOrm",
        backref="channels",
        foreign_keys="ChannelOrm.user_id",
        uselist=False,
        lazy="selectin",
    )


class ChannelOrmRelatedModel:
    __abstract__ = True

    channel_id = Column(
        ForeignKey(
            f"{ChannelOrm.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )


__all__ = ["ChannelOrm", "ChannelOrmRelatedModel"]
