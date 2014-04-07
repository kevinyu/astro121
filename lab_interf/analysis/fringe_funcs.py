import numpy as np


def fringe_freq(B, wl, dec, ha):
    return B * np.cos(dec) * np.cos(ha) / wl
