"""This code uses can be used to convert wavelengths to RGB.

.. note:: Based on Dan Bruton's code:
          http://www.physics.sfasu.edu/astro/color/spectra.html

"""


class ColorGenerator:
    """Color generator class provides different functions for cosmic source
    color estimation."""
    _visual_range = (380.*10**-9, 750.*10**-9)

    @staticmethod
    def spectrum_to_rgb(spectrum, gamma=0.8, float_values=False):
        """
        This function receives an ElectromagneticSpectrum object and returns
        color as RGB tuple. It uses :func:`ColorGenerator.wavelength_to_rgb`
        for a sample of spectrum points and returns an average value. This is
        more precise method than just determining a color using Wien's law.

        If the whole spectrum lies beyond visual range (380-750nm) then
        it will return zeros.

        :param spectrum: electromagnetic spectrum of a source
        :type spectrum: ElectromagneticSpectrum
        :param gamma: (default=0.8) adjustable coefficient
        :type gamma: float
        :param float_values: if True, then float 0..1 values will be returned

        :return: color in RGB scale, example: [100, 200, 255]
        :rtype: list
        """
        color = [0., 0., 0.]
        for n, (w, i) in enumerate(spectrum.lines[1:]):
            w0, i0 = spectrum.lines[n]
            dw, di = abs(w - w0), abs(i - i0)
            w_a = w0 + 0.5 * dw
            if (w_a < ColorGenerator._visual_range[0] or w_a >
                ColorGenerator._visual_range[1]): continue
            s = (min(i, i0) + 0.5 * di) * dw
            c_point = ColorGenerator.wavelength_to_rgb(
                w_a, gamma, float_values=True)
            color = [c0 + s * cp for c0, cp in zip(color, c_point)]
        photons = sum(color)
        if photons:
            if float_values:
                color = [c / photons for c in color]
                dc = 1.0 - max(color)
            else:
                color = [int(255 * c / photons) for c in color]
                dc = 255 - max(color)
            color = [c + dc for c in color]
        return color

    @staticmethod
    def wavelength_to_rgb(wavelength, gamma=0.8, float_values=False):
        """This fuction converts a given peak wavelength to an approximate RGB
        color value. The wavelength should be from 380 nm through 750 nm
        otherwise it will return zeros (i.e. black color).

        :param wavelength: wavelength of incoming photons in m
        :type wavelength: float
        :param gamma: (default=0.8) adjustable coefficient
        :type gamma: float
        :param float_values: if True, then float 0..1 values will be returned

        :return: color in RGB scale, example: [100, 200, 255]
        :rtype: list
        """
        wavelength *= 10. ** 9.
        if 380. <= wavelength < 440.:
            attenuation = 0.3 + 0.7 * (wavelength - 380.) / (440. - 380.)
            r = ((-(wavelength - 440.) / (440. - 380.)) * attenuation) ** gamma
            g = 0.0
            b = (1.0 * attenuation) ** gamma
        elif 440. <= wavelength < 490.:
            r = 0.0
            g = ((wavelength - 440.) / (490. - 440.)) ** gamma
            b = 1.0
        elif 440. <= wavelength < 510.:
            r = 0.0
            g = 1.0
            b = (-(wavelength - 510.) / (510. - 490.)) ** gamma
        elif 510. <= wavelength < 580.:
            r = ((wavelength - 510.) / (580. - 510.)) ** gamma
            g = 1.0
            b = 0.0
        elif 580. <= wavelength < 645.:
            r = 1.0
            g = (-(wavelength - 645.) / (645. - 580.)) ** gamma
            b = 0.0
        elif 645. <= wavelength < 750.:
            attenuation = 0.3 + 0.7 * (750. - wavelength) / (750. - 645.)
            r = (1.0 * attenuation) ** gamma
            g = 0.0
            b = 0.0
        else:
            r = 0.0
            g = 0.0
            b = 0.0
        if not float_values:
            r = int(255. * r)
            g = int(255. * g)
            b = int(255. * b)
        return [r, g, b]
