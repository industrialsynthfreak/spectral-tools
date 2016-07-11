"""This module provides tests for :py:mod:`spectral.spectrum` module."""

import unittest

from spectral.spectrum import Spectrum


class TestSpectrumClass(unittest.TestCase):

    def setUp(self):
        self._values = ((150, 4200), (200.1, 943.99),
                        (320.3, 536), (420., 656))
        self._values2 = ((150, 4200), (199, 9436),
                         (299.5, 536), (420., 656))

    def test_spectrum_instantiation(self):
        try:
            s = Spectrum(self._values)
        except Exception as err:
            self.fail(msg='Class initialization failed.')

    def test_spectrum_base_class(self):
        s1, s2 = Spectrum(self._values), Spectrum(self._values)
        s3 = Spectrum(self._values2)
        s = s1 + s2
        self.assertEqual(type(s), Spectrum)
        s = s1 - s2
        self.assertEqual(s.maximum[1], 0)
        s = s1 * s2
        self.assertEqual(
            s.maximum[1], max(self._values, key=lambda x: x[1])[1] ** 2)
        with self.assertRaises(ValueError):
            s = s1 + s3
        with self.assertRaises(TypeError):
            s = s1 + 42
        s = s1.resample(s3)
        self.assertEqual(list(s.x_values), list(s3.x_values))

    def test_spectrum_properties(self):
        s = Spectrum(self._values)
        self.assertEqual(s.maximum, max(self._values, key=lambda x: x[1]))
        s_x = s.x_values
        s_y = s.intensities
        data = tuple(zip(s_x, s_y))
        self.assertEqual(data, self._values)


if __name__ == "__main__":
    unittest.main()
