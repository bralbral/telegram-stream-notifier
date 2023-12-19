from .constants import ERRORS_LIMIT
from src.db import DataAccessLayer


async def auto_turn_off(
    dal: DataAccessLayer,
) -> None:
    """
    :param dal:
    :return:
    """

    await dal.auto_turn_off_channels(errors_limit=ERRORS_LIMIT)


__all__ = ["auto_turn_off"]
