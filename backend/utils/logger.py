import logging
import sys
from typing import Optional


def get_logger(
    name: str,
    level: int = logging.INFO,
    log_to_stdout: bool = True
) -> logging.Logger:
    """
    Centralized logger factory for the application.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Prevent duplicate handlers

    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )

    if log_to_stdout:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.propagate = False
    return logger
