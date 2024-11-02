import logging
import sys
from core.app_config import config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
        },
        "access": {
            "format": "%(levelname)s: %(client_addr)s - \"%(request_line)s\" %(status_code)s",
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "default",
        },
        "access": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "access",
        },
    },
    "loggers": {
        "app": {"handlers": ["default"], "level": config.DEFAULT_APP_LOGLEVEL, "propagate": False},
        "uvicorn": {"handlers": ["default"], "level": "INFO","propagate": False},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        "apscheduler": {"handlers": ["default"], "level": "INFO", "propagate": False},
    },
}


logging.config.dictConfig(LOGGING_CONFIG)
logger=logging.getLogger("app")  
