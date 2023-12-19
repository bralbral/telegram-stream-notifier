from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from src.logger import logger


async def check_if_need_send_instead_of_edit(
    bot: Bot,
    message_id: Optional[int],
    from_chat_id: int,
    to_chat_id: int,
    delta_messages: int = 3,
) -> bool:
    """
    :param to_chat_id:
    :param bot:
    :param message_id:
    :param from_chat_id:
    :param delta_messages:
    :return:
    """
    if not message_id:
        return True

    deep: int = 20

    result = []

    for i in range(1, deep, 1):
        try:
            message_id_to_check = message_id + i
            await bot.copy_message(
                chat_id=to_chat_id,
                from_chat_id=from_chat_id,
                message_id=message_id_to_check,
                disable_notification=True,
                allow_sending_without_reply=True,
            )
            result.append(1)
        except TelegramBadRequest as ex:
            await logger.ainfo(f"{ex}")
            result.append(0)

    if sum(result) >= delta_messages:
        return True
    else:
        return False


__all__ = ["check_if_need_send_instead_of_edit"]
