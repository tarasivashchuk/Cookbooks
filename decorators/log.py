import logging
from sys import stdout

logging.basicConfig(stream=stdout, level=logging.INFO)


def log_output(func):

    def wrapper():
        logger = logging.getLogger(func.__name__)
        output = func()
        logger.info(output)

    return wrapper


@log_output
def test_function():
    return print("Log me!")


if __name__ == '__main__':
    test_function()
