import time
import logging

logger = logging.getLogger('ws_client')


def timeit(func):
    def wrapped(*args, **kwargs):
        time_start = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        logger.warning(f'{func.__name__} - {time_end - time_start} sec')
        return result
    return wrapped
