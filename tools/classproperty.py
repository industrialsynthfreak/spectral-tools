"""This module provides class property decorator"""


class _ClassPropertyDescriptor:
    def __init__(self, func):
        self._func = func

    def __get__(self, instance, owner):
        return self._func.__func__(owner)


def classproperty(func):
    """Use this as class property decorator"""

    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return _ClassPropertyDescriptor(func)
