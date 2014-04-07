"""Process 3C144 data"""

import numpy as np

import matplotlib.pyplot as plt

from fringe_funcs import fringe_freq
from lsq import fit_components
from objects import OBJECTS
from utils import FourierFilter, Analyzer, bessel, find_indexes_of_zero_crossings


B = 10.0
wl = 3e8 / 10.67e9

datafile = "../data/3C144-4_3_2014-23.npz"
logfile = "../data/logs/3C144-4_3_2014-23-log"

crab = Analyzer(datafile, logfile, dt=1.0, ra=24. * OBJECTS["3C144"]["ra"] / (2. * np.pi))

# First we set invalid points (from telescope homing) to the avg_dc
crab.flatten_invalid_points()

crab["volts_orig"] = crab["volts"]
# Next we find the min and max fringe frequencies that we expect to see in the data
# divide it into chunks since the fringe frequency changes over time
local_fringe_frequencies = fringe_freq(10.0, 0.025, OBJECTS["3C144"]["dec"], 2.*np.pi*crab["ha"]/24.)
min_freq = np.min(abs(local_fringe_frequencies))
print min_freq
# min_freq = 40.0 # rad^-1 (seen by eye as the limit of good data)
max_freq = np.max(abs(local_fringe_frequencies))
print max_freq

# These frequencies are in rad^-1, so to apply the filter we must convert the time array to radians
bandpass = FourierFilter(min_freq=min_freq, max_freq=max_freq)
crab["volts"] = np.real(bandpass(2.0*np.pi*crab["t"]/86164., crab["volts"])[1])
crab["volts"] = crab["volts"] / sorted(crab["volts"])[-10]

crab.flatten_invalid_points()
crab["volts"] = crab["volts"] / np.max(abs(crab["volts"]))

catalog_dec = OBJECTS["3C144"]["dec"]
decs_to_try = np.arange(catalog_dec - np.deg2rad(10.0), catalog_dec + np.deg2rad(10.0), np.deg2rad(0.01))

s2s = []
Y_s = []
for dec in decs_to_try:
    # print "trying %s out of %s" % (dec, len(decs_to_try))
    a, Y_, s2, cov = fit_components(crab["ha"], crab.binned, # crab["volts"],
        lambda ha: np.cos(2*np.pi*(B/wl) * np.cos(dec) * np.sin(2.*np.pi*ha/24.)),
        lambda ha: - np.sin(2*np.pi*(B/wl) * np.cos(dec) * np.sin(2.*np.pi*ha/24.))
    )
    s2s.append(s2)
    Y_s.append(Y_)

measured_dec = decs_to_try[np.argmin(s2s)]


s2s2 = []
Y_s2 = []
B_to_try = np.arange(1.0, 20.0, 0.01)
for baseline in B_to_try:
    a, Y_, s2, cov = fit_components(crab["ha"], crab.binned, #crab["volts"],
        lambda ha: np.cos(2*np.pi*(baseline/wl) * np.cos(catalog_dec) * np.sin(2.*np.pi*ha/24.)),
        lambda ha: - np.sin(2*np.pi*(baseline/wl) * np.cos(catalog_dec) * np.sin(2.*np.pi*ha/24.))
    )
    s2s2.append(s2)
    Y_s2.append(Y_)

measured_B = B_to_try[np.argmin(s2s2)]
