from aiogram.types import BotCommand


def superuser_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command="promote", description="Promote user to admin."),
        BotCommand(command="revoke", description="Revoke admin rights."),
    ]
    return commands


def admin_commands() -> list[BotCommand]:
    commands = [
        BotCommand(command="channels", description="Start Channels Administration"),
    ]
    return commands


__all__ = ["admin_commands", "superuser_commands"]
