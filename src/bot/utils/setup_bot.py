from aiogram import Bot
from aiogram.types import BotCommandScopeChat
from sulguk import AiogramSulgukMiddleware

from ...constants import VERSION
from ..commands import admin_commands
from ..commands import user_commands
from src.config import BotConfig


async def setup_bot(
    config: BotConfig, admins_id: list[int], users_id: list[int]
) -> Bot:
    """
    :param users_id:
    :param admins_id:
    :param config:
    :return:
    """
    bot: Bot = Bot(
        token=config.token.get_secret_value(),
    )

    # https://github.com/Tishka17/sulguk#example-for-aiogram-users
    bot.session.middleware(AiogramSulgukMiddleware())

    await bot.delete_my_commands()

    for _id in users_id:
        await bot.set_my_commands(
            user_commands(), scope=BotCommandScopeChat(chat_id=_id)
        )

    for _id in admins_id:
        await bot.set_my_commands(
            user_commands() + admin_commands(),
            scope=BotCommandScopeChat(chat_id=_id),
        )
        await bot.send_message(chat_id=_id, text=f"Starting bot, version: {VERSION}")

    await bot.delete_webhook()
    return bot


__all__ = ["setup_bot"]
