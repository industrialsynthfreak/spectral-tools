"""This program shows how blackbody spectrum is constructed.

Requires matplotlib."""

import matplotlib.pyplot as plt
from spectral.blackbody import BlackbodySpectrumConstructor
from spectral.color_tools import ColorGenerator

stars = {
    'Sun': 5777.,
    'Sirius': 9940.,
    'Antares': 3200.,
    'GD 165B': 1800.,
    'Spica': 22400.,
    'Luhman 16B': 1210.,
    'WR142': 200000.,
}

plot_x_range_nm = 1100
plot_y_range = int(10 ** 21)
w_max = plot_x_range_nm * 10 ** -9

red_nm = 380.
blue_nm = 750.


def create_star_with_color():
    BlackbodySpectrumConstructor.set_precision(500)
    s = BlackbodySpectrumConstructor(t)
    c_avg = ColorGenerator.spectrum_to_rgb(s, float_values=True)
    return s, c_avg


def _prepare_plot():
    plt.figure(figsize=(16, 9))
    ax = plt.subplot(111)

    ax.set_axis_bgcolor('black')

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.set_yscale('log')
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.xlim(0, w_max)
    x_ticks = [x * 10 ** -9 for x in range(0, plot_x_range_nm, 100)]
    plt.xticks(x_ticks, range(0, plot_x_range_nm, 100))

    plt.ylabel(r"Surface Flux Density, $W * m^{-2} * nm^{-1}$")
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


def _create_plot(s, c_avg, name):
    plt.plot(list(s.x_values), list(s.intensities), color=c_avg)
    mx = s.maximum
    if mx[1] > plot_y_range:
        tx = (mx[0] + 10 ** -8, mx[1])
    elif mx[0] > w_max:
        v = s.get_value(w_max)
        mx = (w_max, v)
        tx = (w_max - 10 ** -7, v * 2)
    else:
        tx = (mx[0], mx[1] * 2)
    plt.annotate(name, xy=mx, xytext=tx, color=c_avg)


if __name__ == "__main__":
    print('''
    List of stars plotted. As you can see, cold and very hot stars have most
    of their spectrum outside the visible range, but hot stars compensate it
    with bigger flux density.
    ''')
    _prepare_plot()

    for name, t in stars.items():
        print('%10s %7.0f K' % (name, t))
        s, c_avg = create_star_with_color()
        _create_plot(s, c_avg, name)

    plt.show()
    plt.close()
