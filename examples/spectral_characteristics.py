import math

from spectral.blackbody import BlackbodySpectrumConstructor
from spectral.color_tools import ColorGenerator

stars = {
    'Sun': (5777., 1.0),
    'Sirius': (9940., 1.71),
    'Antares': (3200., 883.),
    'Spica': (22400., 7.4),
    'Proxima Centauri': (3042., 0.141),
}

sun_radius = 695.7 * 10**6
sun_luminosity_constant = 3.828 * 10**26 / (6.09 * 10**18)
sun_lum_total = 3.828 * 10**26


def create_star(t, r):
    A = 4. * math.pi * (sun_radius * r)**2.
    BlackbodySpectrumConstructor.set_precision(300)
    s = BlackbodySpectrumConstructor(t)
    sm = s.maximum[0] * 10**9
    l_total = s.integrate()
    l_vis_rel = s.relative_visual_intensity
    a_total = l_total * A / sun_lum_total
    a_vis = a_total * l_vis_rel
    l_total /= sun_luminosity_constant
    l_vis = l_total * l_vis_rel
    return s, sm, l_total, l_vis_rel, l_vis, a_total, a_vis


if __name__ == '__main__':
    print('''
    This example shows how to calculate luminosity. To determine the total
    luminosity you of course need to determine star surface i.e. star's radius
    first. The radii of given stars in this example are pre-defined, but there
    are certain formula to calculate them directly.
    ''')

    for name, (t, r) in stars.items():
        s, sm, l_total, l_vis_rel, l_vis, a_total, a_vis = create_star(t, r)
        print('%18s: %5.0f K, '
              'Wmax: %3.0f nm, '
              'Rad Total: %6.2f of sun, '
              'Rad Visible: %5.2f of sun, '
              'Lum Total: %8.2f of sun, '
              'Lum Vis: %8.2f of sun.'
              % (name, t, sm, l_total, l_vis, a_total, a_vis))
