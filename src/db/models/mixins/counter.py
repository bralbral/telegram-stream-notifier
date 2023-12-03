import sqlalchemy as sa


class CounterMixin:
    """Mixin that define count column."""

    __abstract__ = True

    __count_name__ = "count"

    count = sa.Column(
        __count_name__, sa.BigInteger, nullable=True, default=1, index=True
    )


__all__ = ["CounterMixin"]
