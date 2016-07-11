"""This module provides interpolation some basic algorithms.

Available methods are: line, none and point. Line is the linear interpolation,
point is the point sampling, none means that no interpolation at all will be
performed and the first value greater than x will be returned.

**Example**:
::

    >>>from spectral.interpolation import Interpolation
    >>>Interpolation.available_methods
    ('line', 'none', 'point')
    >>>data = [(0, 53.2), (4.1, 24.3), (5.2, -41), (51, 8.0)]
    >>>x = 3.1
    >>>Interpolation.interpolate(data, x, method='line')
    31.348780487804877

"""

import functools

from tools.classproperty import classproperty

_methods = dict()


def _register_interpolation_function(f):
    """Decorates :class:`Interpolation` methods which should be registered
    as interpolation algorithms."""
    _methods[f.__name__] = f

    @functools.wraps(f)
    def wrapper(*args):
        return f.__func__(*args)

    return wrapper


class Interpolation:
    """Class containing some basic interpolation methods.

    Should not be instantiated.

    To use this call :func:`Interpolation.interpolate` method with arguments.

    To register new interpolation method :func:`_interpolation_function`
    module scope decorator is used. The decorator insures, that the method will
    be listed in `Interpolation.methods` dict and in module `_methods` dict.
    """
    # TODO: add cubic and cos algorithms
    _methods = _methods

    @classproperty
    def available_methods(cls):
        """Lists names of all registered methods of interpolation.

        :return: tuple of interpolation method names
        :rtype: tuple of str
        """
        return tuple(cls._methods.keys())

    @classmethod
    def interpolate(cls, values, x, method='none'):
        """Returns a function value for a given point, interpolating between
        given data set (spectrum) points.

        Though you can use interpolation methods directly by calling them
        it is better to use method name as a parameter in this function
        because this provides checks on method availability and etc.

        .. warning:: List of given points should be sorted from smaller to
                     greater *x* numbers.

        .. note:: Interpolation adds startpoint and endpoint to data provided
                  with (-Inf, data[0][1]) and (Inf, data[-1][1]) otherwise
                  off-range values calculation would cause errors.
                  It doesn't modify the data source.

        :param values: list of (x, y) pairs
        :type values: list, tuple of (numeric, numeric)
        :param x: point where a function need to be calculated
        :type x: float, int
        :param method: default is 'none', interpolation method
        :type method: str

            *Values:*
                    - line - A classic line interpolation. Approximates points
                    with a linear function. Doesn't provide smoothness.
                    - point - This method returns *y* value of the point in
                    data, where *x* coordinate is closer to a given *x*.
                    - none - This method just returns the first data list pair
                    y value, where x is greater than a provided *x* parameter.
                    Thus this method is somehow similar to the `point`, except
                    that it doesn't determine which point of the data is closer
                    to a provided *x*.

        :return: y value for given x, if None is returned, than the problem is
            likely to be in provided data.
        :rtype: float, int, None

        :raises ValueError: if interpolation method is not registered
        in the class.
        """
        if method not in cls._methods:
            raise ValueError(
                "%s interpolation method not available."
                "Should be one of these: %s"
                % (method, ', '.join(cls.available_methods)))
        values = cls._add_endpoints(values)
        return cls._methods[method](values, x)

    @staticmethod
    def _add_endpoints(values):
        """Private method which adds -Inf and Inf points to a provided dataset.
        """
        return [(float('-Inf'), values[0][1]), *values,
                (float('Inf'), values[-1][1])]

    @staticmethod
    @_register_interpolation_function
    def none(values, x):
        """Basic interpolation method (no interpolation).
        """
        y1 = None
        for i in range(1, len(values) + 1):
            x1, y1 = values[i]
            if x > x1:
                continue
            break
        return y1

    @staticmethod
    @_register_interpolation_function
    def point(values, x):
        """Point sampling.
        """
        for n, (x1, y1) in enumerate(values[1:]):
            x0, y0 = values[n]
            if x > x1:
                continue
            if x1 - x <= x - x0:
                y = y1
            else:
                y = y0
            return y
        else:
            return None

    @staticmethod
    @_register_interpolation_function
    def line(values, x):
        """Linear interpolation.
        """
        for n, (x1, y1) in enumerate(values[1:]):
            x0, y0 = values[n]
            if x > x1:
                continue
            if y0 == y1:
                return y0
            else:
                y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
                return y
        else:
            return None
