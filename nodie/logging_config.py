"""Centralized logging configuration for the nodie library."""

import logging

# Создаем корневой logger для всей библиотеки
_library_logger: logging.Logger | None = None


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the library.

    Args:
        name: Name of the module requesting the logger (usually __name__)

    Returns:
        Configured logger instance

    Example:
        >>> from nodie.logging_config import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.warning("Something happened")
    """
    # Все логгеры будут дочерними от 'nodie'
    return logging.getLogger(f"nodie.{name}")


def setup_library_logger(
    level: int = logging.WARNING,
    format_string: str | None = None,
    handler: logging.Handler | None = None,
) -> None:
    """Configure the library's root logger.

    This function is intended for library users who want to enable logging.
    By default, the library uses NullHandler and produces no output.

    Args:
        level: Logging level (e.g., logging.DEBUG, logging.INFO)
        format_string: Custom format string for log messages
        handler: Custom handler (if None, uses StreamHandler)

    Example:
        >>> from nodie.logging_config import setup_library_logger
        >>> import logging
        >>> setup_library_logger(level=logging.DEBUG)
    """
    global _library_logger

    if _library_logger is None:
        _library_logger = logging.getLogger("nodie")

    # Очищаем существующие handlers
    _library_logger.handlers.clear()

    # Устанавливаем уровень
    _library_logger.setLevel(level)

    # Создаем handler
    if handler is None:
        handler = logging.StreamHandler()

    # Устанавливаем формат
    if format_string is None:
        format_string = "%(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)

    _library_logger.addHandler(handler)
    _library_logger.propagate = False


def disable_library_logging() -> None:
    """Disable all logging from the library.

    Example:
        >>> from nodie.logging_config import disable_library_logging
        >>> disable_library_logging()
    """
    logger = logging.getLogger("nodie")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())
    logger.setLevel(logging.CRITICAL + 1)  # Выше всех уровней


# Инициализируем NullHandler по умолчанию (best practice для библиотек)
_root_logger = logging.getLogger("nodie")
_root_logger.addHandler(logging.NullHandler())
