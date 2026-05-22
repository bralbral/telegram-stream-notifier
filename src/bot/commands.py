from aiogram.types import BotCommand


def admin_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command="add_user", description="Add user to bot."),
        BotCommand(command="scheduler_start", description="Start scheduler."),
        BotCommand(command="scheduler_pause", description="Stop scheduler."),
    ]
    return commands


def user_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command="cancel", description="Show help."),
        BotCommand(command="add_channel", description="Add notification channel."),
        BotCommand(command="channels", description="List your subscribed channels."),
    ]
    return commands


__all__ = ["admin_commands", "user_commands"]
