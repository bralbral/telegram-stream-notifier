from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from src.constants import SQLITE_DATABASE_FILE_PATH

engine = create_async_engine(
    f"sqlite+aiosqlite:///{SQLITE_DATABASE_FILE_PATH}", future=True
)


# ================  Sqlite Speedup ==============================
# Event listener function to set performance-related settings
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = MEMORY")
    cursor.execute("PRAGMA cache_size = 10000")
    cursor.close()


# Attach the event listener to the engine
event.listen(engine.sync_engine, "connect", set_sqlite_pragma)
# ================================================================

session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=True
)


__all__ = ["engine", "session_maker"]
