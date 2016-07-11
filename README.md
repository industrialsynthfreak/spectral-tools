# spectral-tools
Stellar spectra generation and processing.

Full documentation - /docs/build/html

This package provides a set of functions to manipulate with spectral data.

Authors: Violet Red
Version: 1.0 2016/07/11

This module currently provides different spectral tools for space spectra
construction and manipulation. See `spectral.examples` subpackage for a set of
example programs (some of them depend on `matplotlib`).

### Examples:

    # non-atmospheric solar energetic spectrum approximation
    from spectral.blackbody import BlackbodySpectrumConstructor
    import matplotlib.pyplot as plt
    s = BlackbodySpectrumConstructor(5777)
    plt.plot(list(s.x_values), list(s.intensities), 'g')
    plt.show()

Look at /examples/ folder for more examples.

### Basic description:

The useful functions are contained in :py:mod:`spectral.blackbody` and
:py:mod:`spectral.color_tools`. Other modules provide tools and base
classes for different purposes. This package uses a small set of tools based
in `tools` folder. It is not a part of the current package.
