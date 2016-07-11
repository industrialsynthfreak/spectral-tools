# spectral-tools
Stellar spectra generation and processing.

Full documentation: [/docs/build/html/](https://github.com/industrialsynthfreak/spectral-tools/tree/master/docs/build/html/spectral-tools)

This package provides a set of functions to manipulate with spectral data.

Authors: Violet Red
Version: 1.0 2016/07/11

This module currently provides different spectral tools for space spectra
construction and manipulation.

### Examples:

    # non-atmospheric solar energetic spectrum approximation
    from spectral.blackbody import BlackbodySpectrumConstructor
    import matplotlib.pyplot as plt
    s = BlackbodySpectrumConstructor(5777)
    plt.plot(list(s.x_values), list(s.intensities), 'g')
    plt.show()

More examples: [/examples/](https://github.com/industrialsynthfreak/spectral-tools/tree/master/examples)

![Screen1](https://raw.githubusercontent.com/industrialsynthfreak/spectral-tools/master/docs/img/spectral/stars_spectra.png "Spectra comparison")

### Basic description:

The useful functions are contained in :py:mod:`spectral.blackbody` and
:py:mod:`spectral.color_tools`. Other modules provide tools and base
classes for different purposes. This package uses a small set of tools based
in `/tools/` folder. It is not a part of the current package.
