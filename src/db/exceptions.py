from typing import Optional


class BaseDatabaseException(Exception):
    default_message = "This is a default message!"

    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__(self.default_message)


class DatabaseDoesNotExist(BaseDatabaseException):
    default_message = "You must create database before start. Use 'bash alembic-upgrade.bash' and try again."


class ColumnDoesNotExist(BaseDatabaseException):
    def __init__(self, column: str, table: Optional[str] = None):
        if not table:
            table = ""

        self.default_message = (
            f"Column {column} does not exists. Please check {table} table schema."
        )


__all__ = ["DatabaseDoesNotExist"]
