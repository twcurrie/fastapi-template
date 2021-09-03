from sqlalchemy import create_engine, event  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from app.core.config import settings

engine = create_engine(
    settings.APP_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@event.listens_for(engine, "connect", insert=True)
def set_search_path(db_connection, connection_record):
    """
    This updates the search path to specify a different schema.
    """
    existing_autocommit = db_connection.autocommit
    db_connection.autocommit = True
    cursor = db_connection.cursor()
    cursor.execute(f"SET SESSION search_path='{settings.POSTGRES_SCHEMA}'")
    cursor.close()
    db_connection.autocommit = existing_autocommit


@event.listens_for(engine, "handle_error")
def erase_parameters(exception_context):
    """
    This alters the standard exception raised by SQLAlchemy to remove the 'DETAIL'.
    """
    for exc in [
        exception_context.chained_exception,
        exception_context.original_exception,
        exception_context.sqlalchemy_exception,
    ]:
        if exc is not None:
            exc.args = [exc.args[0].split("\n")[0]]
            if "DETAIL" in exc.args[0]:
                # If DETAIL was not removed by the preceding approach, just redact the entire message.
                exc.args = ["<redacted>"]
