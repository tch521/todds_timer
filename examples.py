from src import Timer
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

@Timer("Example use as a basic decorator")
def basic_example_decorator():
    pass

@Timer("Example use as a decorator with arguments {0} and {1}")
def example_decorator_with_args(a, b):
    pass

@Timer("Example use as a decorator with kwargs {kwarg1} and {kwarg2:.2f}")
def example_decorator_with_kwargs(kwarg1=None, kwarg2=None):
    pass

@Timer("Example use with a mix of args and kwargs {0} and {kwarg1}")
def example_decorator_with_mix_args_kwargs(a, kwarg1=None):
    pass

@Timer("Example use showing timer is accurate to {0} seconds")
def example_1sec(a: int):
    sleep(a)

@Timer("Example use as decorators demonstrating indentation")
def example_decorator_with_indentation():
    basic_example_decorator()


if __name__=="__main__":
    with Timer("Example use as a context manager"):
        pass
    with Timer("Example use as context manager indent 1"):
        with Timer("Example use as context manager indent 2"):
            pass

    basic_example_decorator()
    example_decorator_with_args(1, 2)
    example_decorator_with_kwargs(kwarg1="hello", kwarg2=3.14159)
    example_decorator_with_mix_args_kwargs(1, kwarg1="hello")
    example_1sec(1)
    example_decorator_with_indentation()
    Timer.print_average_times()
