import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "ai-travel-planner")
LOG_DIRECTORY = os.getenv("LOG_DIRECTORY", "logs")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

APP_LOGGER_NAME = APP_NAME.replace(" ", "_").lower()


def setup_logging():
    log_directory = Path(LOG_DIRECTORY)
    log_directory.mkdir(parents=True, exist_ok=True)

    log_filename = f"{APP_LOGGER_NAME}_{datetime.now().strftime('%d_%b_%Y').upper()}.log"
    log_file = log_directory / log_filename

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(module)s.%(funcName)s:%(lineno)d | %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )

    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    root_logger.setLevel(LOG_LEVEL)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name=None):
    return logging.getLogger(name or APP_LOGGER_NAME)