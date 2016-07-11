"""This module provides classes for electromagnetic spectrum manipulations.
"""

import math

from .spectrum import Spectrum
from .filter import SpectrumFilter
from .constructor import SpectrumConstructor

WIEN_C = 2.8977729 * 10**-3  # wien's displacement law constant in m * K
H = 6.63 * 10.**-34.  # J/s planck
C = 299792458.  # m/s light speed
C2 = C * C  # m2/s2 speed of light squared
K = 1.38 * 10.**-23.  # J/K boltzmann


class ElectromagneticSpectrum(Spectrum):
    """The main reason for this type is to provide type matching between
    electromagnetic spectra and forbid arithmetic operations between different
    types of spectra.

    .. py:attribute:: bands

    Data set on bands of electromagnetic spectra. Includes all ranges from
    gamma-rays to radio-waves.
    """
    _nm = 10. ** -9.
    _mm = 10. ** -3.
    _km = 10. ** 3.
    _pm = 10. ** -12.
    bands = {
        'GAMMA': (0., 0.01 * _nm),
        'HX': (0.01 * _nm, 0.1 * _nm),
        'SX': (0.1 * _nm, 10 * _nm),
        'EUV': (10 * _nm, 100 * _nm),
        'FUV': (100 * _nm, 200 * _nm),
        'MUV': (200 * _nm, 300 * _nm),
        'NUV': (300 * _nm, 380 * _nm),
        'VIS': (380 * _nm, 750 * _nm),
        'NIR': (750 * _nm, 1400 * _nm),
        'SIR': (1400 * _nm, 3000 * _nm),
        'MIR': (3000 * _nm, 8000 * _nm),
        'LIR': (8000 * _nm, 15000 * _nm),
        'FIR': (15000 * _nm, 100000 * _nm),
        'THF': (0.1 * _mm, 1. * _mm),
        'EHF': (1. * _mm, 10 * _mm),
        'SHF': (10 * _mm, 100 * _mm),
        'UHF': (100 * _mm, 1),
        'VHF': (1, 10),
        'HF': (10, 100),
        'MF': (100, 1 * _km),
        'LF': (1 * _km, 10 * _km),
        'VLF': (10 * _km, 100 * _km),
        'ULF': (100 * _km, 1000 * _km),
        'SLF': (1000 * _km, 10000 * _km),
        'ELF': (10000 * _km, 100000 * _km)
    }

    def get_intensity_in_band(self, band_name):
        """Returns intensity for a given band range.

        :param band_name: spectral band identifier, see
            :func:`ElectromagneticSpectrum.bands`
        :type band_name: str

        :return: absolute value of flux density on a surface for a given band
        :rtype: float
        """
        return self.integrate(*self.bands[band_name])

    @property
    def relative_visual_intensity(self):
        """Returns intensity in a visual range compared to overall intensity.

        :return: relative visual intensity value 0..1
        :rtype: float
        """
        return self.get_intensity_in_band('VIS') / self.integrate()


class ElectromagneticSpectrumConstructor(SpectrumConstructor):
    """An abstract class for electromagnetic spectrum constructors.
    """

    @classmethod
    def set_spectral_range_by_bands(cls, band1, band2=None):
        """Sets spectral range of the constructor. All constructed spectra will
        have this spectral range.

        You may provide band names listed in
        :py:attr:`spectral.blackbody.ElectromagneticSpectrum.bands` to define
        the spectral range. Note, that some derived constructor classes may
        override this value or even ignore it.

        :param band1: minimal value
        :type band1: str
        :param band2: maximum value, if None, then the full range of band1 will
            be taken
        :type band2: str, None

        :raises ValueError: if any band is not present in
            :py:mod:`constants.constants` or when band1 wavelength >
            band2 wavelength
        """
        band1 = ElectromagneticSpectrum.bands.get(band1)
        if band2:
            band2 = ElectromagneticSpectrum.bands.get(band2)
            if not band1 and not band2:
                raise ValueError(
                    "Wrong EM band name. Valid band names are: %s."
                    % ', '.join(ElectromagneticSpectrum.bands.keys())
                )
        if not band2:
            b1, b2 = band1
        else:
            b1, b2 = band1[0], band2[1]
        if b1 >= b2:
            raise ValueError(
                "Wrong spectral range, because %s "
                "has higher wavelengths than %s" % (band1, band2))
        cls._spectrum_range = (b1, b2)


class BlackbodySpectrumConstructor(ElectromagneticSpectrumConstructor):
    """This class provides simple black body spectrum construction.

    The constructor accepts temperature value, because black body spectrum
    depends only on its temperature (google Planck distribution).

    It can be used for good approximations of normal star radiation spectra
    (see figures).

    Spectral boundaries will be defined automatically. You may modify the
    range manually by setting all checks mentioned above to *False* and by
    :py:meth:`.constructor.SpectrumConstructor.set_spectral_range` or
    :py:meth:`ElectromagneticSpectrumConstructor.set_spectral_range_by_bands`
    but it's not recommended.

    The class uses progressive scale
    (see :py:attribute:`.constructor.SpectrumConstructor.progressive_scale`)
    with tick size
    related to wavelength. At lower wavelengths ticks will be more frequent.
    Set better precision with
    :py:meth:`.constructor.SpectrumConstructor.set_precision`
    method if you are concerned about it. Default precision is 200 points.

    The constructor will try to define maximum of the spectrum using
    Wien's law (again, google it) and locate 99.9% of the total flux inside
    constructed data. :py:attribute:`spectrum_gate` contains boundary values
    relative to a spectral maximum wavelength.

    If :py:attr:`ignore_visual` is not set (as by default), then the
    constructor tries to predict when visual range is needed by comparing
    provided temperature with :py:attr:`visual_t_gate` boundaries.
    By default, these values are set to represent the range from a transition
    between L and T brown dwarfs to a hot Wolf-Rayet star surface temperature.
    Typical objects, exceeding this limit may be neutron stars or ultra-cold
    brown dwarfs and rogue planets. There is no need to include them, because
    their visible luminosity would be negligible.
    If the constructor proceeds, it looks at :py:attr:`visible_range`.
    By default, they also include Near-IR and Near-UV bands.

    .. figure:: ../img/spectral/EffectiveTemperature_300dpi_e.png
                :target: ../img/spectral/EffectiveTemperature_300dpi_e.png
                :align: center
                :width: 10em

        Actual solar extraterrestrial spectrum vs black body spectrum.

    .. figure:: ../img/spectral/spectra-compared.gif
                :target: ../img/spectral/spectra-compared.gif
                :align: center
                :width: 10em

        Example of how stellar spectrum changes with temperature.

    :param temperature: black body surface temperature in kelvins
    :type temperature: float

    :return: electromagnetic spectrum of a black body with given temperature
    :rtype: ElectromagneticSpectrum

    :raises ValueError: if provided temperature <= 1
    """
    _spectrum_type = ElectromagneticSpectrum
    progressive_scale = True
    spectrum_gate = (0.156, 7.8)
    ignore_visual = False
    visual_t_gate = (1199., 250000.)
    visible_range = (ElectromagneticSpectrum.bands['NUV'][0],
                      ElectromagneticSpectrum.bands['NIR'][1])
    _spectrum_range = (ElectromagneticSpectrum.bands['EUV'][0],
                       ElectromagneticSpectrum.bands['NIR'][1])
    _precision = 200

    _k0 = 2. * math.pi * H * C2
    _k1 = H * C / K

    @classmethod
    def _func(cls, wavelength, temperature):
        """Private spectrum construction function.

        Constructs intensity for given wavelength and temperature using
        Planck distribution.

        :param wavelength: specific wavelength (must be >= 10**-10 m)
            .. note:: the function has overflow protection, but it would break
                      the distribution in an overflow ranges
        :type wavelength: float
        :param temperature: temperature of a radiating surface
        :type temperature: float

        :return: intensity value
        :rtype: float
        """
        p = cls._k1 / temperature / wavelength
        p = min(700, p)
        exp = math.exp(p)
        flux = cls._k0 / (wavelength**5. * exp)
        return flux

    @classmethod
    def _define_spectral_range(cls, temperature):
        """Defines spectral range, where 99% of spectrum will be located.
        From 0.01% left to 99% right by wavelength.

        This function uses Wien's law for maximum amplitude wavelength and then
        simply takes 0.312 * lmax left and 7.8 * lmax right borders
        (0.312 and 7.8 coefficients are stored in `_spectrum_gate` class
        attribute).

        Next if `_ignore_visual` is enabled, it will check if temperature lies
        within `_visual_t_gate`. If yes, then it will determine whether vis
        range is included inside boders and shift them if needed.

        :param temperature: temperature in K
        :type temperature: float
        :returns: border range in m
        :rtype: tuple of float, float
        """
        wien_max = WIEN_C / temperature
        k0, k1 = cls.spectrum_gate
        w0, w1 = wien_max * k0, wien_max * k1
        if not cls.ignore_visual:
            t0, t1 = cls.visual_t_gate
            if t0 < temperature < t1:
                vis0, vis1 = cls.visible_range
                if w0 > vis0:
                    w0 = vis0
                if w1 < vis1:
                    w1 = vis1
        return w0, w1

    @staticmethod
    def __new__(cls, temperature):
        if temperature <= 1.:
            raise ValueError(
                "Temperature must be positive. Got %f" % temperature)
        cls.set_spectral_range(*cls._define_spectral_range(temperature))
        return super().__new__(cls, temperature)


class RayleighFilter(SpectrumFilter):
    """This class provides a Rayleigh scattering filter.

    :param spectrum: spectrum to be filtered
    :type spectrum: ElectromagneticSpectrum
    :param mat_abundances: normalized list of material relative abundances
                           in given medium (atmosphere, ocean, etc.).
                           Abundances should be provided as a list of pairs:
                           (Material, relative_molecule_abundance). Note, that
                           often some sources give mass abundances: in this
                           case you should manually convert them using known
                           molar weights.
                           Material instance or class should probide given
                           attributes and methods:
                                - refractive_index(wavelength, temperature)
                                  usually ~1.0 for gases at normal conditions
                                - v - molecule volume in cubic meters
                            See :py:mod:`spectral.mock_material` for more info.
    :type mat_abundances: tuple, list of (Material, float)
    :param molecules: absolute number of molecules on a light's path
    :type molecules: int
    :param temperature: should be > 1K. It's probably better to take an
                        average temperature of the dense atmosphere layer or
                        to create different filters for different atmospheric
                        layers.

    :return: filtered spectrum
    :rtype: ElectromagneticSpectrum
    """
    # TODO: Too low impact on intensity.
    _k = 200000. * 24. * math.pi**3.

    @staticmethod
    def _func(spectrum_x_y, filter_x_y, args):
        """Private function calculating rayleigh scattering effect for a given
        (wave, intensity) point.

        Rayleigh scattering uses common formula
        (see http://plaza.ufl.edu/dwhahn/
            Rayleigh%20and%20Mie%20Light%20Scattering.pdf
        for example):

        I = I0 * sigma / r**2, where
        sigma = 24 * Pi**3 * ((n**2 - 1) / (n**2 + 2))**2 / lambda**4 * N**2
        N - molecules/m3 i.e. concentration of molecules
        because r * N gives us a number of molecules in an atmosphere column
        it can be rewritten as I = I0 * sigma_mod / dN**2
        where dN is a number of molecules in an atmosphere column (which should
        be provided as argument).
        Scattering is meant to be isotropic and non-polarized (for simplicity).
        It is assumed, that half of the radiation escapes to the space.
        """
        w, y0 = spectrum_x_y
        mat_abundances, molecules, t = args
        w4 = w**4.
        sigma_total = 0.
        for mat, c in mat_abundances:
            n2 = mat.refractive_index(w, t)**2
            mod = mat.v**2 * RayleighFilter._k * ((n2 - 1) / (n2 + 2))**2 / w4
            sigma_total += mod * c
        return y0 * max(0., 1. - sigma_total * molecules)

    @staticmethod
    def __new__(cls, spectrum, mat_abundances, molecules, temperature):
        return super().__new__(
            cls, spectrum, None, mat_abundances, molecules, temperature)


class PhotoAbsoprtion(SpectrumFilter):
    """This class provides photoelectric absorption filters.
    It may be useful for atmospheric filtering in case of really hard spectra
    of blue stars where significant amounts of x-ray radiation are present.
    Probably most of the rays with lambda > 10nm won't pierce through any
    common atmosphere at all.

    .. note:: Photoelectric absorption slightly depends on temperature, so
              a minimal required energy (i.e. maximum wavelength) will be
              shifted in a hot medium.

    :param spectrum: spectrum to be filtered
    :type spectrum: ElectromagneticSpectrum
    :param mat_abundances: normalized list of material relative abundances
                           in given medium (atmosphere, ocean, etc.).
                           Abundances should be provided as a list of pairs:
                           (Material, relative_molecule_abundance). Note, that
                           often some sources give mass abundances: in this
                           case you should manually convert them using known
                           molar weights.
                           Material instance or class should probide given
                           attributes and methods:
                                - photoeffect_cross_section(wavelength,
                                temperature) in m3, usually < 10**-30
                            See :py:mod:`spectral.mock_material` for more info.
    :type mat_abundances: tuple, list of (Material, float)
    :param molecules: absolute number of molecules on a light's path
    :type molecules: int
    :param temperature: should be > 1K. It's probably better to take an
                        average temperature of the dense atmosphere layer or
                        to create different filters for different atmospheric
                        layers.

    :return: filtered spectrum
    :rtype: ElectromagneticSpectrum
    """
    @staticmethod
    def _func(spectrum_x_y, filter_x_y, args):
        """Private function calculating resulting beam intensity after the
        photoelectric absorption process.
        """
        w, y0 = spectrum_x_y
        mat_abundances, molecules, t = args
        sigma = 0.
        for mat, c in mat_abundances:
            sigma += c * mat.photoeffect_cross_section(w, t)
        return y0 * math.exp(-molecules * sigma)

    @staticmethod
    def __new__(cls, spectrum, mat_abundances, molecules, temperature):
        return super().__new__(
            cls, spectrum, None, mat_abundances, molecules, temperature)
