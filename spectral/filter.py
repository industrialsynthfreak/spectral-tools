"""Provides abstract base class
:class:`spectral.filter.SpectrumFilter` for spectral data manipulations.
"""

from itertools import repeat
from multiprocessing.pool import Pool

from spectral.spectrum import Spectrum


class SpectrumFilter:
    """Abstract class for implementing different types of spectral filters.

    It is a constructor class, i.e. instantiation of this class returns new
    Spectrum instance with modified data.

    If filter_spectrum is provided, then at first it will resample filter
    spectrum to match the processing spectrum. Then it will send spectrum
    data points to a multiprocessing pool to be modified by
    :func:`SpectrumFilter._func` with related filter points as first argument
    and rest of args as the second argument. Then args will be umpacked the
    way programmer defined it in the function. Returned data will be combined
    into a new spectrum and send back as a return value.

    See _func docstring for more info.

    :func:`SpectrumFilter._func` actually is the only method to be redefined in
    derived classes.

    :param spectrum: spectrum to be processed
    :type spectrum: Spectrum
    :param filter_spectrum: filter spectrum (default: None)
    :type filter_spectrum: Spectrum, None
    :param args: any additional values and constants

    :return: new processed spectrum
    :rtype: Spectrum
    """

    @staticmethod
    def _func(spectrum_x_y, filter_x_y, args):
        """Private method to be redefined in actual class.

        .. warning:: This method is expected to be redefined in actual classes.

        ..note:: Please use the same function parameters as here, otherwise
                 you need to redefine :meth:`SpectrumFilter._process` and
                 __new__ methods.

        :param spectrum_x_y: a point from an initial spectrum
        :type spectrum_x_y: list, tuple of (numeric, numeric)
        :param filter_x_y: a point from a resampled filter spectrum
        :type filter_x_y: list, tuple of (numeric, numeric)
        :param args: list of additional parameters (coefficients and constants)
        :type args: list, tuple

        :return: intensity (amplitude) value for a specific conditions.
            Usually it should be x coordinate (wavelength) and some parameter.
        :rtype: float

        :raises NotImplementedError: if you try to access to it in an abstract
            base class :class:`SpectrumConstructor`.
        """
        raise NotImplementedError(
            "Trying to call abstract class function.")
        return float()

    @classmethod
    def _process(cls, spectrum, filter_spectrum, *args):
        """This private class method process spectrum with a given filter
        and parameters.

        .. note:: If no filter spectrum is provided, then it passes None as
                  filter spectrum point to all processes.

        This method uses multiprocessing.
        """
        if filter_spectrum:
            resampled_filter_spectrum = filter_spectrum.resample(spectrum)
            resampled_filter_lines = resampled_filter_spectrum.lines
        else:
            resampled_filter_lines = repeat(None, len(spectrum.lines))
        data = zip(spectrum.lines, resampled_filter_lines, repeat(args))
        p = Pool()
        y_values = p.starmap(cls._func, data)
        p.close()
        p.join()
        lines = zip(spectrum.x_values, y_values)
        return type(spectrum)(lines, interpolation=spectrum.interpolation)

    @staticmethod
    def __new__(cls, spectrum, filter_spectrum=None, *args):
        spectrum = cls._process(spectrum, filter_spectrum, *args)
        return spectrum
