from functools import wraps
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

def check_element_exist(f):
    @wraps(f)
    def func(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            return result
        except AttributeError:
            logger.error(f'Article {args[1]} has no searched element')
            result = ''
            return result
    return func