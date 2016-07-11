"""This module provides tests for :py:mod:`spectral.constructor` module."""

import unittest

from spectral.constructor import SpectrumConstructor


class TestSpectrumConstructorAbstractClass(unittest.TestCase):
    def test_spectrum_constructor_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            c = SpectrumConstructor()


if __name__ == "__main__":
    unittest.main()
