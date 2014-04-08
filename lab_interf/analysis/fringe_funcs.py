import numpy as np


def fringe_freq(B, wl, dec, ha):
    return B * np.cos(dec) * np.cos(ha) / wl


def bessel(fR):
    N = 1000.
    MF = np.zeros(len(fR))
    return sum(
            np.sqrt(1. - (n/N)**2.) *
            np.cos(2.0*np.pi*fR*n/N)
            for n in np.arange(-N, N)
    )
