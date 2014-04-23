import numpy as np


c = 3e5  # km/s
f_0 = 1.420  # GHz


# inputs
R = 15. # kpc (radius of galaxy)


def v1(r):
    return 200.


def profile(d, v, x0=None, n=100):
    depth = np.sqrt(R**2. - d**2.)
    if not x0 or (x0 <= -depth):
        x0 = -depth
    bins = np.linspace(x0, depth, n)
    freqs = []
    for x in bins:
        r = np.sqrt(x**2 + d**2)
        v_los = v(r) * d / r
        f = f_0 * (v_los / c)
        freqs.append(f)
    return freqs
