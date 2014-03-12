import numpy as np


def rekt(long_, lat):
    return np.array([
        np.cos(lat) * np.cos(long_),
        np.cos(lat) * np.sin(long_),
        np.sin(lat)
    ])


# (RA, DEC) to (HA, DEC)
R_rd2hd = lambda LST: np.array([
    [np.cos(LST), np.sin(LST), 0],
    [np.sin(LST), -np.cos(LST), 0],
    [0, 0, 1]
])

# (HA, DEC) to (AZ, ALT)
R_hd2aa = lambda lat: np.array([
    [-np.sin(lat), 0, np.cos(lat)],
    [0, -1, 0],
    [np.cos(lat), 0, np.sin(lat)]
])

# (AZ, ALT) to (l, b)
R_aa2lb = np.array([
    [-0.054876, -0.873437, -0.483835],
    [0.494109, -0.444830, 0.746982],
    [-0.867666, -0.198076, 0.455984]
])


def unrekt(xp):
    return np.arctan2(xp[1], xp[0]), np.arcsin(xp[2])


def rd2aa(ra, dec, lst=None, lat=None):
    """Convert a RA, DEC to AZ, ALT

    ra : right ascension of object of interest (radians)
    dec : declination of object of interest (radians)
    lst : local sidereal time of observer (radians)
    lat : latitude of observer (radians)

    Returns az and alt in radians"""
    x = rekt(ra, dec)
    x = np.dot(R_rd2hd(lst), x)
    x = np.dot(R_hd2aa(lat), x)
    return unrekt(x)
