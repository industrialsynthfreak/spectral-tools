"""This program demonstrates the way filters work.

Requires matplotlib.
"""

import math

import matplotlib.pyplot as plt
from spectral.blackbody import BlackbodySpectrumConstructor, RayleighFilter
from spectral.color_tools import ColorGenerator

# Defining atmospheric gases.


class Element:
    def __init__(self):
        self.name = str()
        self.symbol = str()
        self.z = int()
        self.a = int()
        self.r_waals = float()
        self.I = float()

    @property
    def q(self):
        return self.z * 1.60217662 * 10.**-19.

    @property
    def m(self):
        return self.a * 1.660539040 * 10.**-27.

    @property
    def v(self):
        return 4 / 3 * math.pi  * self.r_waals**3

    @property
    def photoeffect_cross_section(self):
        return 0.23 * (5.29 * 10**-11)**2. / self.z**2.

    def photoeffect_wavelength_threshold(self, temperature=0.):
        l = 6.63 * 10.**-34. * 299792458. / (
            self.I + 1.38 * 10.**-23. * temperature)
        return l


class Molecule:

    def __init__(self):
        self.elements = list()
        self.name = str()
        self.symbol = str()
        self._ref_a = float()
        self._ref_b = float()
        self._ref_c = float()
        self._v = None
        self.spectrum = None

    @property
    def molar_mass(self):
        return sum((e.a for e in self.elements))

    @property
    def v(self):
        if self._v:
            return self._v
        return sum((e.v for e in self.elements))

    def photoeffect_cross_section(
            self, wavelength, temperature, energy_dependent=False):
        cross_section = 0.
        for e in self.elements:
            l_max = e.photoeffect_wavelength_threshold(temperature)
            if l_max > wavelength:
                sigma = e.photoeffect_cross_section
                if energy_dependent:
                    sigma *= (wavelength / l_max)**3.5
                cross_section += sigma
        return cross_section

    def refractive_index(self, wavelength, temperature):
        wavelength *= 10.**6.
        d = self._ref_a + self._ref_b / (self._ref_c - wavelength**2)
        d *= (temperature / 293.15)
        return 1.0 + d


N = Element()
N.z = 7
N.a = 14
N.r_waals = 155. * 10.**-12.
N.I = 14.53414 * 1.60217662 * 10.**-19.

N2 = Molecule()
N2.name = 'Nitrogen'
N2.elements = [N, N]
N2._ref_a = 6.8552 * 10**-5
N2._ref_b = 3.253157 * 10**-2
N2._ref_c = 144.
N2._v = (364 * 10.**-12.)**3

O = Element()
O.z = 8
O.a = 16
O.r_waals = 152. * 10.**-12.
O.I = 13.61806 * 1.60217662 * 10.**-19.

O2 = Molecule()
O2.name = 'Oxygen'
O2.elements = [O, O]
O2._ref_a = 1.181494 * 10**-4
O2._ref_b = 9.708931 * 10**-3
O2._ref_c = 75.4
O2._v = (346 * 10.**-12.)**3

atmosphere = ((N2, 0.79), (O2, 0.21))

sun_t = 5777.
t_earth = 290.
s = 4 * 3.1415 * (6330 * 1000.)**2
dm = 5.15 * 10 ** 18 / s
molecules = 6.022 * 10 ** 23 * dm * 1000. / 29.04

plot_x_range_nm = 1100
plot_y_range = int(10 ** 13)
w_max = plot_x_range_nm * 10 ** -9

red_nm = 380.
blue_nm = 750.


def prepare_plot():
    plt.figure(figsize=(16, 9))
    ax = plt.subplot(111)

    ax.set_axis_bgcolor('black')

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # ax.set_yscale('log')
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.xlim(0, w_max)
    x_ticks = [x * 10 ** -9 for x in range(0, plot_x_range_nm, 100)]
    plt.xticks(x_ticks, range(0, plot_x_range_nm, 100))

    plt.ylabel(r"Surface Flux Density, $W * m^{-2}$")
    plt.xlabel(r"Wavelength, $nm$")
    plt.suptitle("Electromagnetic spectra of different stars"
                 "\n(black body approximation).", fontsize=16,
                 ha='center')
    plt.figtext(.5, .011, 'For each star color of its curve is equivalent '
                          'to its surface color. Red and blue dotted lines '
                          'represent a visible part of the EM spectrum '
                          '(380 - 750nm).\nStar names are roughly placed at '
                          'intensity maximums.',
                fontsize=12, ha='center')

    plt.plot([red_nm * 10 ** -9] * 10,
             list(range(0, plot_y_range * 10, plot_y_range)),
             '--', color='blue')
    plt.plot([blue_nm * 10 ** -9] * 10,
             list(range(0, plot_y_range * 10, plot_y_range)),
             '--', color='red')


def create_plot(s, c_avg, name):
    plt.plot(list(s.x_values), list(s.intensities), color=c_avg)
    mx = s.maximum
    tx = (mx[0] + 10**-8, mx[1] + 10**12)
    plt.annotate(name, xy=mx, xytext=tx, color=c_avg)


if __name__ == "__main__":
    print('''
    This program demonstrates the way filters work.
    ''')
    prepare_plot()

    BlackbodySpectrumConstructor.set_precision(500)

    s = BlackbodySpectrumConstructor(sun_t)
    c_avg = ColorGenerator.spectrum_to_rgb(s, float_values=True)
    create_plot(s, c_avg, 'outside atmosphere')

    s = RayleighFilter(s, atmosphere, molecules, t_earth)
    c_avg = ColorGenerator.spectrum_to_rgb(s, float_values=True)
    create_plot(s, c_avg, 'after rayleigh ')

    plt.show()
    plt.close()
