import os

import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger(name: str) -> Logger:
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "app.log"
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] (%(module)s.%(filename)s) → %(funcName)s() : Line %(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logger.level)

        # File Handler
        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=5 * 1024 * 1024, backupCount=2
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logger.level)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.propagate = False

    return logger
