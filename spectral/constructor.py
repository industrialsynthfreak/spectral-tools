"""This module provides an abstract class for spectrum constructors.

Each spectrum should be constructed through a specific spectrum constructor,
which would provide valid data.
"""

from tools.classproperty import classproperty
from .spectrum import Spectrum


class SpectrumConstructor:
    """Abstract base class for spectrum constructors.

    It is a constructor class, i.e. instantiation of this class returns new
    Spectrum instance.

    :func:`SpectrumConstructor._func` actually is only method to be redefined.

    `SpectrumConstructor.progressive_scale` boolean parameter controls if x
    axis has progressive linear scale division or not.

    :return: specific spectrum
    :rtype: Spectrum
    """
    _spectrum_range = (100. * 10. ** -9., 1400. * 10. ** -9.)
    _precision = 100
    _spectrum_type = Spectrum
    progressive_scale = False

    @classmethod
    def _func(cls, *args):
        """Private method to be redefined in actual class.

        .. warning:: This method is expected to be redefined in actual classes.

        :returns: intensity (amplitude) value for a specific conditions.
            Usually it should be x coordinate (wavelength) and some parameter.
        :rtype: float

        :raises NotImplementedError: if you try to access to it in an abstract
            base class :class:`spectral.spectrum.SpectrumConstructor`.
        """
        raise NotImplementedError(
            "Trying to call abstract class function.")
        return float()

    @classmethod
    def set_precision(cls, precision):
        """Set spectrum precision, i.e. number of bands (points) in spectrum.

        Precision should be > 2. Common value is 100.

        .. warning:: Do not use it too often because spectra with different
                     sets of points are going to be not compatible or would
                     take significant amount of resources for resampling.

        :param precision: number of points (bands) in a resulting spectrum
        :type precision: int

        :raises ValueError: if precision is not in range 2..1000.
        """
        if precision < 2:
            raise ValueError(
                "Precision must be in range 1 - 1000, but got %d" % precision)
        cls._precision = int(precision)

    @classmethod
    def set_spectral_range(cls, band1, band2):
        """Set new range of generating spectra.

        It is better to use positive values. Negative values support is not
        guaranteed.

        .. warning:: Do not use it too often because spectra with different
                     sets of points are going to be not compatible or would
                     take significant amount of resources for resampling.

        :param band1: minimal value
        :type band1: float
        :param band2: maximum value
        :type band2: float

        :raises ValueError: if band1 >= band2
        """
        if band1 >= band2:
            raise ValueError(
                "Wrong spectral range, because %f "
                "has higher wavelengths than %f" % (band1, band2))
        cls._spectrum_range = (band1, band2)

    @classmethod
    def _return_spectrum(cls, values, *args):
        """Private method which generates intensity values.
        """
        for v in values:
            yield v, cls._func(v, *args)

    @classproperty
    def _wavelist(cls):
        """Private class property returning list of bands (wavelengths)
        i.e. x axis values.
        """

        def _create_progressive_division():
            k = dw / sum((range(cls._precision)))
            s = w_min
            for i in range(cls._precision):
                s += k * i
                yield s

        w_min, w_max = cls._spectrum_range
        dw = w_max - w_min
        if cls.progressive_scale:
            waves = _create_progressive_division()
        else:
            step = dw / cls._precision
            waves = (w_min + step * i for i in range(cls._precision))
        return waves

    @staticmethod
    def __new__(cls, *args):
        """Constructs and returns :class:`Spectrum` instance.
        """
        lines = list(cls._return_spectrum(cls._wavelist, *args))
        return cls._spectrum_type(lines)
