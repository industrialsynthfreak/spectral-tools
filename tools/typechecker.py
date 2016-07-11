"""This module provides a type checker decorator to validate function
arguments."""


def check_types(f):
    """Wrapper which checks types of provided arguments.

    It checks only two first arguments in the function. The basic functionality
    is to provide type matching in redefined arithmetic operations.

    :return: wrapped function
    :rtype function:

    :raises TypeError: on type mismatch.
    """

    def wrapper(owner, other, *args, **kws):
        if not type(owner) == type(other):
            raise TypeError(
                "Type mismatch error: %s and %s" % (type(owner), type(other)))
        return f(owner, other, *args, **kws)

    return wrapper
