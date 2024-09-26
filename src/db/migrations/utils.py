from alembic import op
from sqlalchemy import inspect


# source
#  https://stackoverflow.com/a/71624331
def column_exists(table_name, column_name):
    bind = op.get_context().bind
    insp = inspect(bind)
    columns = insp.get_columns(table_name)
    return any(c["name"] == column_name for c in columns)


__all__ = ["column_exists"]
