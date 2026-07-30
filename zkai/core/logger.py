"""Structured Logging Infrastructure for ZKAI."""

import logging
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path


class StructuredFormatter(logging.Formatter):
    """Custom JSON structured log formatter for machine readability."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        if hasattr(record, "extra_data"):
            log_entry["extra"] = getattr(record, "extra_data")
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


class ColoredFormatter(logging.Formatter):
    """Human-readable ANSI colored log formatter for terminal output."""

    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        time_str = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        msg = f"[{time_str}] [{color}{record.levelname:<8}{self.RESET}] [{record.name}]: {record.getMessage()}"
        if record.exc_info:
            msg += f"\n{self.formatException(record.exc_info)}"
        return msg


class Logger:
    """Encapsulated logger wrapper for ZKAI components."""

    def __init__(self, name: str, level: int = logging.INFO, log_file: Optional[str] = None):
        self._logger = logging.getLogger(f"zkai.{name}")
        self._logger.setLevel(level)
        self._logger.propagate = False

        if not self._logger.handlers:
            # Console Handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(ColoredFormatter())
            self._logger.addHandler(console_handler)

            # Optional File Handler
            if log_file:
                path = Path(log_file)
                path.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(path, encoding="utf-8")
                file_handler.setFormatter(StructuredFormatter())
                self._logger.addHandler(file_handler)

    def debug(self, msg: str, **kwargs: Any) -> None:
        self._logger.debug(msg, extra={"extra_data": kwargs} if kwargs else None)

    def info(self, msg: str, **kwargs: Any) -> None:
        self._logger.info(msg, extra={"extra_data": kwargs} if kwargs else None)

    def warning(self, msg: str, **kwargs: Any) -> None:
        self._logger.warning(msg, extra={"extra_data": kwargs} if kwargs else None)

    def error(self, msg: str, **kwargs: Any) -> None:
        self._logger.error(msg, extra={"extra_data": kwargs} if kwargs else None)

    def critical(self, msg: str, **kwargs: Any) -> None:
        self._logger.critical(msg, extra={"extra_data": kwargs} if kwargs else None)


def get_logger(name: str, level: int = logging.INFO) -> Logger:
    """Factory function to get a named ZKAI logger instance."""
    return Logger(name, level=level)
