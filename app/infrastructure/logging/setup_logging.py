from logging.config import dictConfig

from app.application.models.config import LoggingSettings


def setup_logging() -> None:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "format": "%(asctime)s %(levelname)s %(message)s %(module)s",
                "datefmt": "%Y-%m-%dT%H:%M:%SZ",
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "json",
            }
        },
        "loggers": {
            "": {
                "handlers": ["stdout"],
                "level": LoggingSettings().LOGGING_LEVEL,
            },
            "oauth2client": {
                "handlers": ["stdout"],
                "level": "WARNING",  # Suppress INFO and below for oauth2client
            },
            "transport": {
                "handlers": ["stdout"],
                "level": "WARNING",  # Suppress INFO and below for transport
            },
            "__init__": {
                "handlers": ["stdout"],
                "level": "WARNING",  # Suppress INFO and below for the __init__ module
            },
            "googleapiclient": {  # Add google API client if it's involved in logging.
                "handlers": ["stdout"],
                "level": "WARNING",  # Adjusting for potential third-party libraries
            },
        },
    }
    dictConfig(logging_config)
