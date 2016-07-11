from spectral.blackbody import BlackbodySpectrumConstructor
from spectral.color_tools import ColorGenerator

stars = {
    'Sun': 5777.,
    'Sirius': 9940.,
    'Antares': 3400.,
    'Mintaka': 29500.,
    'OTS44': 1700.,
    'Capella': 4970.,
    'Rigel': 12100.,
    'Spica': 22400.,
    'WR142': 200000.,
}


def create_star():
    BlackbodySpectrumConstructor.set_precision(200)
    s = BlackbodySpectrumConstructor(t)
    sm = s.maximum[0]
    cm = ColorGenerator.wavelength_to_rgb(sm)  # maximum intensity color
    c_avg = ColorGenerator.spectrum_to_rgb(s)  # average color
    r_vis = s.relative_visual_intensity
    return s, sm, r_vis, cm, c_avg


if __name__ == '__main__':
    print('''
    This program compares the two methods of star surface color determination.

    1. RGBmax converts maximum intensity wavelength to a color using
    ColorGenerator.wavelength_to_rg function. As you may see, most hot or cold
    stars maximums are non in the visual range (~400-750nm).
    For extremely hot objects, such as Wolf-Rayet stars, only ~0.3% of light
    emitted is visible.
    Very cold stars, like OTS44 brown dwarf, will emit most of its spectrum in
    Near-IR.

    2. RGBavg uses ColorGenerator.spectrum_to_rgb to calculate average weighted
    color value using all spectrum intensity bands.
    ''')

    for name, t in stars.items():
        s, sm, r_vis, cm, c_avg = create_star()
        print('%10s: %7.0f K, Wmax: %6.1f nm, '
              'LumVis/LumTotal: %5.2f %%, RGB max: %13s, RGB avg: %15s'
              % (name, t, sm * 10**9, r_vis * 100, cm, c_avg))
