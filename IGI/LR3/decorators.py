import functools
import time

def timing_decorator(func):
    """
    A decorator that measures and prints the execution time of the wrapped function.
    Args:
        func (callable): The function whose execution time is to be measured.
    Returns:
        callable: A wrapper function that executes the original function and prints its execution time.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'\033[31;1m[TIMING_DECORATOR] \033[32;1m{func.__name__} выполнена за {end_time - start_time:.3f} секунд\033[0m\n')
        return result
    return wrapper