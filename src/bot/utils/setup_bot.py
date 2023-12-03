from aiogram import Bot
from aiogram.types import BotCommandScopeChat
from sulguk import AiogramSulgukMiddleware

from ..commands import admin_commands
from ..commands import superuser_commands
from src.config import BotConfig


async def setup_bot(
    config: BotConfig, superusers_id: list[int], admins_id: list[int]
) -> Bot:
    """
    :param admins_id:
    :param superusers_id:
    :param config:
    :return:
    """
    bot: Bot = Bot(
        token=config.token.get_secret_value(),
    )

    # https://github.com/Tishka17/sulguk#example-for-aiogram-users
    bot.session.middleware(AiogramSulgukMiddleware())

    await bot.delete_my_commands()

    for _id in admins_id:
        await bot.set_my_commands(
            admin_commands(), scope=BotCommandScopeChat(chat_id=_id)
        )

    for _id in superusers_id:
        await bot.set_my_commands(
            superuser_commands() + admin_commands(),
            scope=BotCommandScopeChat(chat_id=_id),
        )

    await bot.delete_webhook()
    return bot


__all__ = ["setup_bot"]
