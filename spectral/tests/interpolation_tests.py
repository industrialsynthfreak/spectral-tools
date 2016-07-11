"""This module provides tests for :py:mod:`spectral.interpolation` module."""

import unittest

from spectral.interpolation import Interpolation


class TestInterpolationMethods(unittest.TestCase):

    def setUp(self):
        self._values = ((1.1, 4.3), (1.5, 3.1), (3.9, 6.0),
                        (4.5, -12), (10., 19))
        self._def_value = 3.0

    def test_interpolation_algorithms(self):
        I = Interpolation
        self.assertTrue(I.available_methods,
                        msg='No interpolation methods available.')

        with self.assertRaises(ValueError,
                               msg='No exception on non-implemented method.'):
            I.interpolate(
                self._values, self._def_value, method='NOT IMPLEMENTED METHOD')

        for m in I.available_methods:
            msg = 'Wrong interpolation of an off-range point for {}.'.format(m)
            self.assertEqual(I.interpolate(self._values, float('-Inf'), m),
                             self._values[0][1], msg=msg)
            self.assertEqual(I.interpolate(self._values, float('Inf'), m),
                             self._values[-1][1], msg=msg)
            for x, y in self._values:
                self.assertEqual(I.interpolate(self._values, x, m), y)


if __name__ == "__main__":
    unittest.main()
