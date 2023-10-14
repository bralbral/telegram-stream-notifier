from aiogram.types import BotCommand


def superuser_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command="promote", description="Promote user to admin."),
        BotCommand(command="revoke", description="Revoke admin rights."),
    ]
    return commands


def admin_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command="add", description="Add Youtube channel."),
        BotCommand(command="delete", description="Delete Youtube channel."),
        BotCommand(command="list", description="List Youtube channels"),
    ]
    return commands


__all__ = ["admin_commands", "superuser_commands"]
