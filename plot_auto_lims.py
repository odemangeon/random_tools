""" Improve plots by not plotting outliers and just indicate them with an arrow.

This module is heavily inspired by the plots produced by the Everest code: https://github.com/rodluger/everest/
"""

import numpy as np
from collections import Iterable


def auto_y_lims(y, ax, pad=0.1):
    """Define the axis limits on the y axis to show the signal but ignore the obvious outliers.

    :param 1D_iterable y: y values
    :param AxesSubplot ax: matplotlib.axes._subplots.AxesSubplot instance to use.
    :param float/list_of_2_floats pad: pad values to use below and on top of the 99.5% interval limits.
        If to values are provided the first is used for bottom pad and the top used for top pad.
    """
    if isinstance(pad, Iterable):
        if len(pad) == 2:
            pad_low, pad_bottom = pad
        else:
            raise ValueError("pad should be a float of an Iterable of 2 floats.")
    else:
        pad_low = pad_bottom = pad
    # Get y lims that bound 99.5% of the y values
    N = int(0.995 * len(y))
    hi, lo = y[np.argsort(y)][[N, -N]]
    pad_low, pad_bottom = [(hi - lo) * pad for pad in [pad_low, pad_bottom]]
    ylim = (lo - pad_low, hi + pad_bottom)
    ax.set_ylim(ylim)


def indicate_y_outliers(x, y, ax, color=None, masksncolors=None, **kwargs):
    """Indicates y outliers which are off axis by an arrow.

    This function a portion of code extracted from Rodrigo Luger's Everest github repository:
    https://github.com/rodluger/everest/blob/master/everest/user.py

    :param 1D_iterable x: x values
    :param 1D_iterable y: y values
    :param AxesSubplot ax: matplotlib.axes._subplots.AxesSubplot instance to use.
    :param string default_color: String giving the color to use for a normal outliers (not identified
        in a masks provided in masksncolors)
    :param dict masksncolors: Dictionary with keys the name of the mask and values are dictionary themselves
        with up to 3 keys "mask", "color" and "plot".
        "mask" is the only mandatory key. It's values gives the list of indexes in y that masked y values
        for this mask.
        "color" is a string given the color to give to the arrows for these masked values. If color is
        omitted None will passed as color.
        "plot" is a bool that says if you want to plot an arrow for these masked data points that are
        of axis. If plot is ommitted, True is assumed.

    kwargs are passed to arrowprops of annotate
    """
    if masksncolors is None:
        masksncolors = {}
    ylim = ax.get_ylim()
    # Indicate off-axis outliers
    for ii in np.where(y < ylim[0])[0]:
        found_in_mask = False
        plot = True
        for mnc in masksncolors:
            if ii in mnc["mask"]:
                found_in_mask = True
                plot = mnc.get("plot", True)
                if plot:
                    color2use = mnc.get("color", None)
                break
        if not(found_in_mask):
            color2use = color
        ax.annotate('', xy=(x[ii], ylim[0]), xycoords='data',
                    xytext=(0, 10), textcoords='offset points',
                    arrowprops=dict(arrowstyle="-|>", color=color2use, **kwargs))
    for ii in np.where(y > ylim[1])[0]:
        found_in_mask = False
        plot = True
        for mnc in masksncolors:
            if ii in mnc["mask"]:
                found_in_mask = True
                plot = mnc.get("plot", True)
                if plot:
                    color2use = mnc.get("color", None)
                break
        if not(found_in_mask):
            color2use = color
        ax.annotate('', xy=(x[ii], ylim[1]), xycoords='data',
                    xytext=(0, -10), textcoords='offset points',
                    arrowprops=dict(arrowstyle="-|>", color=color2use, **kwargs))
