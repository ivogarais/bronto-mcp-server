import logging
import os
import sys


DEFAULT_LEVEL = "INFO"
DEFAULT_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _resolve_level(level: str | int | None) -> int:
    """Resolve a logging level.

    Parameters
    ----------
    level : str | int | None
        Explicit level value or ``None`` to use environment defaults.

    Returns
    -------
    int
        Resolved logging level as a numeric value.
    """
    if isinstance(level, int):
        return level

    raw_value = (
        level if level is not None else os.getenv("BRONTO_LOG_LEVEL", DEFAULT_LEVEL)
    )
    normalized = str(raw_value).strip().upper()

    if normalized.isdigit():
        return int(normalized)

    resolved = getattr(logging, normalized, None)
    if isinstance(resolved, int):
        return resolved

    return logging.INFO


def bootstrap_logging(level: str | int | None = None, force: bool = False) -> None:
    """Configure root logging for the process.

    Parameters
    ----------
    level : str | int | None, optional
        Optional log level override.
    force : bool, optional
        Whether to replace existing handlers.
    """
    target_level = _resolve_level(level)
    root_logger = logging.getLogger()
    root_logger.setLevel(target_level)

    if root_logger.handlers and not force:
        for handler in root_logger.handlers:
            handler.setLevel(target_level)
        return

    formatter = logging.Formatter(
        fmt=os.getenv("BRONTO_LOG_FORMAT", DEFAULT_FORMAT),
        datefmt=os.getenv("BRONTO_LOG_DATE_FORMAT", DEFAULT_DATE_FORMAT),
    )
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setLevel(target_level)
    stream_handler.setFormatter(formatter)

    if force:
        root_logger.handlers.clear()

    root_logger.addHandler(stream_handler)


def module_logger(module_name: str) -> logging.Logger:
    """Create a module-scoped logger.

    Parameters
    ----------
    module_name : str
        Logger name, usually ``__name__``.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    return logging.getLogger(module_name)
