from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from .user import UserOrmRelatedModel
from src.db.mixins import Base
from src.db.mixins import TimestampsMixin


class ChannelOrm(Base, TimestampsMixin, UserOrmRelatedModel):
    """
    Base
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

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<id={self.id}, url={self.url}>"


class ChannelOrmRelatedModel:
    __abstract__ = True

    channel_id = Column(
        ForeignKey(
            f"{ChannelOrm.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )


__all__ = ["ChannelOrm", "ChannelOrmRelatedModel"]
