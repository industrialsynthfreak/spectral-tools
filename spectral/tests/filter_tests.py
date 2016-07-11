"""This module provides tests for :py:mod:`spectral.filter` module."""

import unittest

from spectral.spectrum import Spectrum
from spectral.filter import SpectrumFilter


class TestFilterAbstractClass(unittest.TestCase):
    def test_filter_is_abstract(self):
        values = ((150, 4200), (200.1, 943.99), (320.3, 536), (420., 656))
        s = Spectrum(values)
        with self.assertRaises(NotImplementedError):
            c = SpectrumFilter(s)


if __name__ == "__main__":
    unittest.main()
