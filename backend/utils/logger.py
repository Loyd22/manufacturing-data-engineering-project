"""
Central logging setup for the manufacturing data platform.

Why this exists:
- keeps logging logic in one place
- makes console messages cleaner and more consistent
- can later be extended to log into files
"""

import logging
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """
    Create or return a configured logger.

    Args:
        name: usually __name__ from the file using the logger
    """
    logger = logging.getLogger(name)

    # Prevent adding duplicate handlers if the logger is requested many times
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Create logs folder if it does not exist yet
    Path("logs").mkdir(exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler("logs/pipeline.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger