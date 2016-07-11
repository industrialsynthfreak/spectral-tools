"""This module provides a base Spectrum class which could be used to store
and process different types of spectral band data.
"""

from multiprocessing.pool import Pool

from .interpolation import Interpolation
from tools.typechecker import check_types


class Spectrum:
    """This is a class-container for common spectral date.

    The class stores list of bands. It is recommended to construct the
    instances only through :class:`spectral.constructor.SpectrumConstructor`
    classes, which is able to validate lines. It is also recommended not to
    modify lines data directly but only with
    :class:`spectral.filter.SpectrumFilter` classes.

    Spectrum class provides basic arithmetic operations between its instances,
    such as: sum, multiplication and subtraction, but these operations only
    provided for spectra with matching x values.

    .. :note:: Spectra can be summed, subtracted one from another or multiplied

    :param lines: list of (value, intensity) pairs. Actual spectral data is
        stored here, you may use it directly, but it's not recommended. Lines
        will be sorted in order of first value in pairs when instance is
        constructed.
    :type lines: list of (value, intensity) pairs.
    :param interpolation: default is 'point', determines interpolation type to
        be used with :class:`spectral.interpolation.Interpolation` methods.
    :type interpolation: str
    """

    def __init__(self, lines, interpolation='point'):
        self.lines = list(lines)
        self.lines.sort(key=lambda x: x[0])
        self.lines = tuple(self.lines)
        self.interpolation = interpolation

    def get_value(self, x):
        """Returns value for a given x coordinate. It uses interpolation
        algorithm. Uses :class:`interpolation.Interpolation`.

        :param x: coordinate
        :type x: int, float

        :return: point with
        :rtype: float
        """
        return Interpolation.interpolate(self.lines, x, self.interpolation)

    def integrate(self, x0=None, x1=None):
        """Integrates a spectrum in a specified range.

        :param x0: bottom border
        :type x0: float, None
        :param x1: top border
        :type x1: float, None

        .. note:: if x0 or/and x1 not specified or None, then minimum value of
                  the spectrum will be taken for x0 and/or maximum value will
                  taken for x1.

        :return: sum inside given range
        :rtype: float, int

        :raises ValueError: if x0 > x1
        """
        # 1.01 to compensate gate effect
        return sum((i for w, i in self._yield_integrated_bins(x0, x1)))

    @property
    def maximum(self):
        """This property returns maximum value of the spectrum.

        This property doesn't use interpolation and returns point in a spectrum
        with max value.

        :return: band, containing max value
        :rtype: (float, float)
        """
        return max(self.lines, key=lambda x: x[1])

    @property
    def x_values(self):
        """Returns a generator containing all x values of spectrum lines.

        :return: x values
        :rtype: generator of float
        """
        for (x, y) in self.lines:
            yield x

    @property
    def intensities(self):
        """Returns a generator containing all intensities presented in lines.

        :return: y values
        :rtype: generator of float
        """
        for (x, y) in self.lines:
            yield y

    @check_types
    def resample(self, other):
        """Resampling which uses bands from another spectrum.

        This procedure may be resource heavy, so it isn't automatically
        executed before arithmetic operations with two spectra. Use it manually
        by yourself when needed.

        This function uses multiprocessing.

        .. note:: This procedure preserves interpolation algorithm from the
                  parent spectrum.

        :param other: sample spectrum
        :type other: Spectrum

        :return: new spectrum compatible with other
        :rtype: Spectrum
        """
        p = Pool()
        y_values = p.map(self.get_value, other.x_values)
        p.close()
        p.join()
        lines = zip(other.x_values, y_values)
        return type(self)(lines, interpolation=self.interpolation)

    def _yield_integrated_bins(self, x0, x1):
        """This private method is used to provide integrated columns of
        the spectrum as a generator.

        This is a private function for different type of spectral summs.
        It provides validation check and summs data. You should not use this
        function directly. Use :func:`Spectrum.integrate` instead.
        """
        if not x0:
            x0 = self.lines[0][0]
        if not x1:
            x1 = self.lines[-1][0]
        if x0 > x1:
            raise ValueError(
                "Range must be valid, got x0 > x1, %f > %f" % (x0, x1))
        for n, (w, i) in enumerate(self.lines[1:]):
            if w < x0:
                continue
            w0, i0 = self.lines[n]
            dw = w - w0
            w_avg = w0 + dw * 0.5
            i1 = self.get_value(w_avg) * dw
            if w >= x1:
                break
            yield (w_avg, i1)

    @check_types
    def __add__(self, other):
        """Sums two spectra and returns a new one.

        For example, it may be used to create a binary star spectrum or a
        planet spectrum (because the latter not only reflects sunlight but also
        radiates heat itself).
        In case of a protostar with a accretion disk the overall spectrum will
        be a sum of the protostar core radiation and the disk radiation.

        :param other: other spectrum
        :type other: Spectrum

        :return: new spectrum
        :rtype: Spectrum
        """
        new_lines = []
        for (s1_x, s1_y), (s2_x, s2_y) in zip(self.lines, other.lines):
            if s1_x != s2_x:
                raise ValueError("Spectral lines of given spectra do not"
                                 "match each other.")
            new_lines.append((s1_x, s1_y + s2_y))
        return type(self)(new_lines, interpolation=self.interpolation)

    @check_types
    def __sub__(self, other):
        """Subtracts one spectrum from another.

        .. warning:: below zero results will be converted to zero, because
                     there is no usual need for them. If you actually want a
                     strange behaviour you may manipulate with lines attribute
                     directly.

        :param other: other spectrum
        :type other: Spectrum

        :return: new spectrum
        :rtype: Spectrum
        """
        new_lines = []
        for (s1_x, s1_y), (s2_x, s2_y) in zip(self.lines, other.lines):
            if s1_x != s2_x:
                raise ValueError("Spectral lines of given spectra do not"
                                 "match each other.")
            new_lines.append((s1_x, max(s1_y - s2_y, 0)))
        return type(self)(new_lines, interpolation=self.interpolation)

    @check_types
    def __mul__(self, other):
        """Multiplies spectral values.

        It may be used to filter a spectrum, although because most of intensity
        attenuation laws are complex, it is better to use
        :class:`spectral.filter.SpectrumFilter` derived classes for this.

        :param other: other spectrum
        :type other: Spectrum

        :return: new spectrum
        :rtype: Spectrum
        """
        new_lines = []
        for (s1_x, s1_y), (s2_x, s2_y) in zip(self.lines, other.lines):
            if s1_x != s2_x:
                raise ValueError("Spectral lines of given spectra do not"
                                 "match each other.")
            new_lines.append((s1_x, s1_y * s2_y))
        return type(self)(new_lines, interpolation=self.interpolation)
