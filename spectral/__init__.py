"""This package provides a set of functions to manipulate with spectral data.

:Authors: Violet Red
:Version: 1.0 2016/07/11

This module currently provides different spectral tools for space spectra
construction and manipulation. See `spectral.examples` subpackage for a set of
example programs (some of them depend on `matplotlib`).

**Examples:**
::

    # non-atmospheric solar energetic spectrum approximation
    from spectral.blackbody import BlackbodySpectrumConstructor
    import matplotlib.pyplot as plt
    s = BlackbodySpectrumConstructor(5777)
    plt.plot(list(s.x_values), list(s.intensities), 'g')
    plt.show()

**Basic description:**

The useful functions are contained in :py:mod:`spectral.blackbody` and
:py:mod:`spectral.color_tools`. Other modules provide tools and base
classes for different purposes. This package uses a small set of tools based
in `tools` folder. It is not a part of the current package.
"""

import spectral.blackbody as blackbody
import spectral.constructor as constructor
import spectral.filter as filter
import spectral.interpolation as interpolation
import spectral.spectrum as spectrum
import spectral.color_tools as wavelength_to_rgb

__version__ = '1.0'
