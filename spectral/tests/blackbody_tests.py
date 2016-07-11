"""This module provides tests for :py:mod:`spectral.blackbody` module."""

import unittest

from spectral.blackbody import (BlackbodySpectrumConstructor,
                                RayleighFilter, PhotoAbsoprtion)
from spectral.mock_material import MockMaterial


class TestBlackbodyClasses(unittest.TestCase):

    def setUp(self):
        r = 6330 * 1000.
        s = 4 * 3.1415 * r * r
        dm = 5.5 * 10**18 / s
        self.molecules = 6.03 * 10**23 * dm * 1000. / 29.04
        self.elements = ((MockMaterial(), 0.79), (MockMaterial(), 0.21))
        self.t = 5777

    def test_blackbody_spectrum(self):
        solar = BlackbodySpectrumConstructor(self.t)
        f = RayleighFilter(solar, self.elements, self.molecules, self.t)
        self.assertAlmostEqual(solar.maximum[0] * 10 ** 6, 0.5, places=1)
        self.assertLess(f.maximum[1], solar.maximum[1],
                        msg="Rayleigh filter doesn't seem to work")
        p = PhotoAbsoprtion(solar, self.elements, self.molecules, self.t)
        self.assertLess(p.maximum[1], solar.maximum[1],
                        msg="Photo-absorption filter doesn't seem to work")


if __name__ == "__main__":
    unittest.main()
