import enum

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import TypeDecorator
from sqlalchemy import UniqueConstraint

from .mixins import ModelORM
from .mixins import RepresentationMixin


# source
# https://gist.github.com/hasansezertasan/691a7ef67cc79ea669ff76d168503235
class IntEnum(TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """

    impl = Integer
    cache_ok = True

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class ChannelTypeEnum(enum.IntEnum):
    YOUTUBE = 1
    TWITCH = 2


class ChannelTypeORM(ModelORM, RepresentationMixin):
    """
    Model for storing YT channels
    """

    __tablename__ = "channel_types"

    __table_args__ = (UniqueConstraint("type", name="ix_uniq_type"),)
    # some features with autoincrement
    # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#allowing-autoincrement-behavior-sqlalchemy-types-other-than-integer-integer
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    type = Column(
        IntEnum(ChannelTypeEnum),
        nullable=False,
        index=True,
        default=ChannelTypeEnum.YOUTUBE,
    )


class ChannelTypeORMRelatedModel:
    __abstract__ = True

    channel_type_id = Column(
        ForeignKey(
            f"{ChannelTypeORM.__tablename__}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        default=ChannelTypeEnum.YOUTUBE,
    )


__all__ = ["ChannelTypeEnum", "ChannelTypeORM", "ChannelTypeORMRelatedModel", "IntEnum"]
