import os
import logging
from tenacity import (
    after_log,
    before_log,
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_fixed,
)

from typing import Optional

from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_attempts = int(os.environ.get("DB_STARTUP_MAX_ATTEMPTS", 5))
max_delay_seconds = float(os.environ.get("DB_STARTUP_MAX_DELAY_SECONDS", 60 * 5))
wait_seconds = int(os.environ.get("DB_STARTUP_WAIT_SECONDS", 1))


@retry(
    stop=(
        stop_after_attempt(max_attempt_number=max_attempts)
        | stop_after_delay(max_delay=max_delay_seconds)
    ),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db: SessionLocal) -> None:
    try:
        db.execute("SELECT 1")  # Try to create session to check if DB is awake
    except Exception as e:
        logger.error(e)
        raise e


def main(_session: Optional[SessionLocal] = None) -> None:
    logger.info("Initializing service")
    init(db=_session or SessionLocal())
    logger.info("Service finished initializing")


if __name__ == "__main__":  # pragma: no cover
    main()
