import os
import sys
from pathlib import Path

from loguru import logger


def database_log_filter(record):
    return "postgres" in record["name"]


# is called from main.py
def set_logger():
    log_folder = Path(__file__).parent / "logs"
    log_folder.mkdir(exist_ok=True, parents=True)

    logger.remove()

    log_level = "DEBUG" if os.getenv("STAGE") == "DEBUG" else "INFO"

    # set logging file for app
    logger.add(log_folder / "app.log", rotation="10 MB", retention="7 days", level=log_level, enqueue=True)

    # set logging file for postgres interactions
    logger.add(
        log_folder / "database.log",
        filter=database_log_filter,
        rotation="10 MB",
        retention="7 days",
        level=log_level,
        enqueue=True,
    )

    # set logging in terminal
    logger.add(sys.stderr, level=log_level, colorize=True)
