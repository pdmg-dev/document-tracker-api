# app/core/logger.py

import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings


class RelativePathFormatter(logging.Formatter):
    def __init__(self, *args, root: Path = Path.cwd(), **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root.resolve()

    def format(self, record: logging.LogRecord) -> str:
        full_path = Path(record.pathname).resolve()
        try:
            relative_path = full_path.relative_to(self.root)
        except ValueError:
            relative_path = full_path.name
        record.filepath = str(relative_path)
        return super().format(record)


def get_logger(name: str) -> Logger:
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / settings.log_file
    log_level = settings.log_level.upper()

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    if not logger.handlers:
        formatter = RelativePathFormatter(settings.log_format, datefmt=settings.log_datefmt)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logger.level)

        # File Handler
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logger.level)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.propagate = False

    return logger
