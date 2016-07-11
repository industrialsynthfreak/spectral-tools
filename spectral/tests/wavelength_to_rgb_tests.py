"""This module provides tests for :py:mod:`spectral.wavelength_to_rgb` module.
"""

import unittest

from spectral.color_tools import ColorGenerator


class TestWavelengthToRgb(unittest.TestCase):
    def test_warnings(self):
        with self.assertWarns(RuntimeWarning):
            x = ColorGenerator.wavelength_to_rgb(100 * 10**-9)
            self.assertEqual(x, (0, 0, 0))

    def test_output_datatype(self):
        x = ColorGenerator.wavelength_to_rgb(500 * 10**-9)
        for i in x:
            self.assertEqual(type(i), int)

    def test_adequate_output(self):
        x = ColorGenerator.wavelength_to_rgb(400 * 10**-9)
        y = ColorGenerator.wavelength_to_rgb(700 * 10**-9)
        self.assertGreater(sum(x), 0)
        self.assertGreater(sum(y), 0)


if __name__ == "__main__":
    unittest.main()
