import logging
import pathlib
from logging.handlers import RotatingFileHandler

from decouple import config  # type: ignore

def bootstrap_logger() -> logging.Logger:
    enabled = config("QUALYSPY_LOG_ENABLED", default="False", cast=bool)
    log_file = str(config("QUALYSPY_LOG_FILE", default=pathlib.Path.home() / "qualyspy.log"))
    level_name = str(config("QUALYSPY_LOG_LEVEL", default="INFO")).upper()
    rotate_mb = config("QUALYSPY_LOG_MAX_MB", default=10, cast=int)
    backups = config("QUALYSPY_LOG_BACKUPS", default=5, cast=int)
    datefmt = "%Y-%m-%d %H:%M:%S"


    logger = logging.getLogger("qualyspy")
    if logger.handlers:  # protect against double-initialisation
        return logger
    
    if not enabled:
        logger.addHandler(logging.NullHandler())
        logger.setLevel(logging.CRITICAL)    # silence by default
        logger.propagate = False
        return logger

    logger.setLevel(level_name)

    if rotate_mb == 0:  # allow “no rotation” by env
        handler = logging.FileHandler(log_file, encoding="utf-8")
    else:
        handler = RotatingFileHandler(
            log_file,
            maxBytes=rotate_mb * 1024 * 1024,
            backupCount=backups,
            encoding="utf-8",
        )

    fmt = (
        "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
    )
    handler.setFormatter(logging.Formatter(fmt, datefmt))
    logger.addHandler(handler)
    logger.propagate = False  # don’t spam root logger
    return logger
