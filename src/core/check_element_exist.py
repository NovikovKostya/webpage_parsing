import logging
from functools import wraps

logger = logging.getLogger(__name__)


def check_element_exist(f):
    @wraps(f)
    def func(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            return result
        except Exception:
            logger.error(f'Article {args[1]} has no searched element')
            result = ''
            return result

    return func
