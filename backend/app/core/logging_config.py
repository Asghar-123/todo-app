import logging
import sys
from logging.config import dictConfig

def configure_logging():
    """
    Configures application-wide logging.
    """
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelname)s:     %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelname)s:     %(client_addr)s - "%(request_line)s" %(status_code)s',
                "use_colors": None,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": sys.stderr,
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": "INFO"},
            "uvicorn.error": {"level": "INFO", "handlers": ["default"]},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
            "backend": {"handlers": ["default"], "level": "INFO", "propagate": False}, # Custom logger for our application
        },
        "root": {"handlers": ["default"], "level": "INFO"},
    }
    dictConfig(LOGGING_CONFIG)

    # Get our custom logger
    app_logger = logging.getLogger("backend")
    app_logger.info("Logging configured.")
    return app_logger

# Initialize logger for use throughout the application
logger = configure_logging()
