"""Mock material class to provide a general structure of material type needed
for electromagnetic filters.
"""


class MockMaterial:
    """Mock material class provides an interface for material classes
    construction to be compatible with electromagnetic filters of the package.

    It is also used in unit tests.
    """

    def refractive_index(self, wavelength, temperature):
        """Refractive index of the material.

        :param wavelength: light wavelength in m
        :param temperature: medium temperature in kelvins

        :return: differential cross-section
        :rtype: float
        """
        return 1.001

    def photoeffect_cross_section(self, wavelength, temperature):
        """Photoelectric effect cross-section in square meters.

        :param wavelength: light wavelength in m
        :param temperature: medium temperature in kelvins

        :return: differential cross-section
        :rtype: float
        """
        return 10**-34.

    @property
    def v(self):
        """Molecule volume in cubic meters."""
        return 10**-30.
