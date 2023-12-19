from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from .mixins import ModelOrm
from .mixins import RepresentationMixin
from .mixins import TimestampsMixin


class UserOrm(ModelOrm, TimestampsMixin, RepresentationMixin):
    """
    Model for storing TG users
    """

    __tablename__ = "users"

    __table_args__ = (UniqueConstraint("user_id", name="ix_uniq_telegram_user_id"),)
    # some features with autoincrement
    # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#allowing-autoincrement-behavior-sqlalchemy-types-other-than-integer-integer
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id = Column(BigInteger, nullable=False, index=True)
    username = Column(String(length=255), nullable=True, index=True)
    firstname = Column(String(length=255), nullable=True, index=True)
    lastname = Column(String(length=255), nullable=True, index=True)
    is_superuser = Column(Boolean, default=False, index=True)


class UserOrmRelatedModel:
    __abstract__ = True

    user_id = Column(
        ForeignKey(
            f"{UserOrm.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )


__all__ = ["UserOrm", "UserOrmRelatedModel"]
