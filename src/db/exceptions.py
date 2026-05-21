from typing import Optional


class BaseDatabaseException(Exception):
    default_message = "This is a default message!"

    def __init__(self, *args):
        if args:
            super().__init__(*args)
        else:
            super().__init__(self.default_message)


class DatabaseDoesNotExist(BaseDatabaseException):
    default_message = (
        "Database connection failed. Ensure PostgreSQL is running and "
        "DATABASE_HOST, DATABASE_PORT, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME are set correctly."
    )


class ColumnDoesNotExist(BaseDatabaseException):
    def __init__(self, column: str, table: Optional[str] = None):
        if not table:
            table = ""

        self.default_message = (
            f"Column {column} does not exists. Please check {table} table schema."
        )


__all__ = ["ColumnDoesNotExist", "DatabaseDoesNotExist"]
