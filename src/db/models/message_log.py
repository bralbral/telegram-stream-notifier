from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from .mixins import ModelOrm
from .mixins import RepresentationMixin
from .mixins import TimestampsMixin


class MessageLogOrm(ModelOrm, TimestampsMixin, RepresentationMixin):
    """
    Model for storing id of actual post message
    """

    __tablename__ = "message_logs"

    __table_args__ = (UniqueConstraint("message_id", name="ix_uniq_message_id"),)

    # some features with autoincrement
    # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#allowing-autoincrement-behavior-sqlalchemy-types-other-than-integer-integer
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    message_id = Column(BigInteger, nullable=False, index=True)
    text = Column(String, nullable=False, index=False)


__all__ = ["MessageLogOrm"]
