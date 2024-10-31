from enum import Enum
import logging
from datetime import datetime
from typing import Optional


class LogLevel(Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


class ProgressLogger:
    # ANSI color codes
    COLORS = {
        LogLevel.INFO: "\033[36m",     # Cyan
        LogLevel.SUCCESS: "\033[32m",   # Green
        LogLevel.WARNING: "\033[33m",   # Yellow
        LogLevel.ERROR: "\033[31m",     # Red
        LogLevel.DEBUG: "\033[35m"      # Magenta
    }
    RESET = "\033[0m"

    def __init__(self, name: Optional[str] = None):
        self.logger = logging.getLogger(name or __name__)
        # Add stream handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _format_message(self, level: LogLevel, message: str) -> str:
        """Format log message with timestamp, color and prefix"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.COLORS[level]}[{timestamp}] {level.value}: {message}{self.RESET}"

    def info(self, message: str):
        """Log info level message"""
        formatted = self._format_message(LogLevel.INFO, message)
        self.logger.info(formatted)

    def success(self, message: str):
        """Log success level message"""
        formatted = self._format_message(LogLevel.SUCCESS, message)
        self.logger.info(formatted)  # Using info level since success is custom

    def warning(self, message: str):
        """Log warning level message"""
        formatted = self._format_message(LogLevel.WARNING, message)
        self.logger.warning(formatted)

    def error(self, message: str):
        """Log error level message"""
        formatted = self._format_message(LogLevel.ERROR, message)
        self.logger.error(formatted)

    def debug(self, message: str):
        """Log debug level message"""
        formatted = self._format_message(LogLevel.DEBUG, message)
        self.logger.debug(formatted)

    def progress(self, message: str, current: int, total: int):
        """Log progress message with percentage"""
        percentage = (current / total) * 100
        progress_message = f"{message} - {percentage:.1f}% ({current}/{total})"
        self.info(progress_message)

    def add_file_handler(self, filepath: str):
        """Add file handler for logging to file"""
        file_handler = logging.FileHandler(filepath)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

    def set_level(self, level: LogLevel):
        """Set minimum logging level"""
        level_map = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR
        }
        self.logger.setLevel(level_map.get(level, logging.INFO))

    def set_format(self, timestamp_format: str = "%Y-%m-%d %H:%M:%S",
                   message_format: str = "[{timestamp}] {level}: {message}"):
        """Set custom message format"""
        self._timestamp_format = timestamp_format
        self._message_format = message_format
