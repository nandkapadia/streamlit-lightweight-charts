"""
Logging configuration for Streamlit Lightweight Charts Pro.

This module provides centralized logging configuration for the package,
including proper log levels, formatting, and handlers.
"""

import logging
import sys
from typing import Optional


def setup_logging(
    level: int = logging.ERROR,
    log_format: Optional[str] = None,
    stream: Optional[logging.StreamHandler] = None,
) -> logging.Logger:
    """
    Set up logging configuration for the package.

    Args:
        level: Logging level (default: INFO)
        log_format: Custom log format string
        stream: Custom stream handler

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("streamlit_lightweight_charts_pro")
    logger.setLevel(level)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Set default format if not provided
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Create stream handler if not provided
    if stream is None:
        stream = logging.StreamHandler(sys.stdout)
        stream.setLevel(level)
        stream.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(stream)

    return logger


def get_logger(name: Optional[str] = None, level: int = logging.ERROR) -> logging.Logger:
    """
    Get a logger instance for the package.

    Args:
        name: Optional logger name (will be prefixed with package name)
        level: Logging level (default: ERROR)
    Returns:
        Logger instance
    """
    logger = logging.getLogger(f"streamlit_lightweight_charts_pro.{name}")
    logger.setLevel(level)
    return logger


# Initialize default logging
setup_logging()
