import logging
from typing import Any, Callable
from functools import wraps


class LLMError(Exception):
    pass


def error_handler(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except LLMError as e:
            logging.error(f"LLM Error: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise
    return wrapper
