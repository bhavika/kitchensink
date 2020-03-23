"""Structured logging for rg-train."""

import structlog
from structlog.stdlib import LoggerFactory


def get_structured_logger(*args, **initial_values):
    """Get a structured logger
    Parameters
    ----------
    name : str
        The logger's name. For example: 'rg-train'.
    Returns
    -------
    structlog.Logger
    """
    structlog.configure(logger_factory=LoggerFactory())
    return structlog.get_logger(*args, **initial_values)
