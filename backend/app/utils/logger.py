import logging
from logging.config import dictConfig

from app.core.config import settings

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": settings.log_level,
        }
    },
    "root": {
        "handlers": ["console"],
        "level": settings.log_level,
    },
}

dictConfig(LOG_CONFIG)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
