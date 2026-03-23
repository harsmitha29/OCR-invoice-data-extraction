"""
logger.py - Logging configuration
"""
import logging
import os

os.makedirs("output", exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "output/application.log",
            "mode": "a",
            "delay": True,
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console", "file"]},
}


def setup_logging():
    import logging.config
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(__name__)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


setup_logging()
