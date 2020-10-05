import logging
from functools import wraps
from sys import stdout

logging.basicConfig(stream=stdout, level=logging.DEBUG)


def log_output(func):

    def wrapper():
        logger = logging.getLogger(func.__name__)
        output = func()
        logger.info(f"Output: {output}")

    return wrapper


def log_args(func):

    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        [logger.info(arg) for arg in args]
        [logger.info(kwarg) for kwarg in kwargs]

        output = func(*args, **kwargs)
        logger.info(f"Output: {output}")

    return wrapper


def log_level(level):

    def inner_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            logger.setLevel(level)
            [logger.info(arg) for arg in args]
            [logger.info(kwarg) for kwarg in kwargs]
            output = func(*args, **kwargs)
            logger.log(msg=f"Output: {output}", level=level)

        return wrapper
    return inner_function


@log_output
def test_function():
    return print("Log me!")


@log_args
def test_args(x):
    return x ** x


@log_level(level=logging.CRITICAL)
def test_level(x):
    return x ** x



if __name__ == '__main__':
    test_function()
    [test_args(value) for value in range(0, 10, 2)]
    [test_level(value) for value in range(0, 10, 2)]
