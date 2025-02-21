import functools
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.warning(f"Attempt {attempts} of {max_attempts} failed: {e}")
            logger.error(f"All {max_attempts} attempts failed.")
            raise
        return wrapper
    return decorator