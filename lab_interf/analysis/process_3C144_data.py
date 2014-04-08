"""Process 3C144 data"""

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

from fringe_funcs import fringe_freq
from lsq import fit_components
from objects import OBJECTS
from utils import FourierFilter, Analyzer


font = dict(
    size = 14
)
matplotlib.rc('font', **font)

B = 10.0
wl = 3e8 / 10.67e9

datafile = "../data/3C144-4_3_2014-23.npz"
logfile = "../data/logs/3C144-4_3_2014-23-log"

crab = Analyzer(datafile, logfile, dt=1.0, ra=24. * OBJECTS["3C144"]["ra"] / (2. * np.pi))

plt.subplot(211)
plt.plot(crab["ha"], crab["volts"])
plt.xlabel(r"Hour angle [h]", fontsize=18)
plt.ylabel(r"Power", fontsize=18)
plt.subplot(212)
trans = np.fft.fft(crab["volts"])
freqs = np.fft.fftfreq(len(trans), 2. * np.pi * 1.0 / 86164.)
plt.plot(np.fft.fftshift(freqs), np.fft.fftshift(abs(trans)**2))
plt.xlabel(r"Frequency [rad$^{-1}$]", fontsize=18)
plt.ylabel(r"Power", fontsize=18)

# First we set invalid points (from telescope homing) to the avg_dc
crab.flatten_invalid_points()

crab["volts_orig"] = crab["volts"]
# Next we find the min and max fringe frequencies that we expect to see in the data
# divide it into chunks since the fringe frequency changes over time
local_fringe_frequencies = fringe_freq(10.0, wl, OBJECTS["3C144"]["dec"], 2.*np.pi*crab["ha"]/24.)
min_freq = np.min(abs(local_fringe_frequencies))
# min_freq = 40.0 # rad^-1 (seen by eye as the limit of good data)
max_freq = np.max(abs(local_fringe_frequencies))

catalog_dec = OBJECTS["3C144"]["dec"]

'''
s2s2 = []
Y_s2 = []
a2s = []
B_to_try = np.arange(5.0, 15.0, 0.01)
for baseline in B_to_try:
    a, Y_, s2, cov = fit_components(crab["ha"], crab.normed, #crab["volts"],
        lambda ha: np.cos(2*np.pi*(baseline/wl) * np.cos(catalog_dec) * np.sin(2.*np.pi*ha/24.)),
        lambda ha: - np.sin(2*np.pi*(baseline/wl) * np.cos(catalog_dec) * np.sin(2.*np.pi*ha/24.))
    )
    s2s2.append(s2)
    Y_s2.append(Y_)
    a2s.append(a)

a2 = a2s[np.argmin(s2s2)]
measured_B = B_to_try[np.argmin(s2s2)]

plt.figure()
plt.plot(B_to_try, s2s2, linewidth=2)
plt.xlabel(r"$B_y$ [m]", fontsize=18)
plt.ylabel(r"$\chi^2$", fontsize=18)

'''

# These frequencies are in rad^-1, so to apply the filter we must convert the time array to radians
bandpass = FourierFilter(min_freq=min_freq, max_freq=max_freq)
# crab.flatten_invalid_points()
# crab["volts"] = crab["volts"] / sorted(crab["volts"])[-10]

# crab.flatten_invalid_points()
# crab["volts"] = crab["volts"] / np.max(abs(crab["volts"]))
crab["volts"] = crab.real_boxcar(200)

plt.figure()
plt.subplot(211)
plt.plot(crab["ha"], crab["volts"])
plt.xlabel(r"Hour angle [h]", fontsize=18)
plt.ylabel(r"Power", fontsize=18)
plt.subplot(212)
trans = np.fft.fft(crab["volts"])
freqs = np.fft.fftfreq(len(trans), 2.*np.pi * 1.0 / 86164.)
plt.plot(np.fft.fftshift(freqs), np.fft.fftshift(abs(trans)**2))
plt.xlabel(r"Frequency [rad$^{-1}$]", fontsize=18)
plt.ylabel(r"Power", fontsize=18)

decs_to_try = np.arange(catalog_dec - np.deg2rad(10.0), catalog_dec + np.deg2rad(10.0), np.deg2rad(0.01))

s2s = []
Y_s = []
a1s = []
for dec in decs_to_try:
    # print "trying %s out of %s" % (dec, len(decs_to_try))
    a, Y_, s2, cov = fit_components(crab["ha"], crab.normed, # crab["volts"],
        lambda ha: np.cos(2*np.pi*(B/wl) * np.cos(dec) * np.sin(2.*np.pi*ha/24.)),
        lambda ha: - np.sin(2*np.pi*(B/wl) * np.cos(dec) * np.sin(2.*np.pi*ha/24.))
    )
    s2s.append(s2)
    Y_s.append(Y_)
    a1s.append(a)

a1 = a1s[np.argmin(s2s)]
measured_dec = decs_to_try[np.argmin(s2s)]

plt.figure()
plt.plot(np.rad2deg(decs_to_try), s2s, linewidth=2)
plt.xlabel(r"$\delta$ [deg]", fontsize=18)
plt.ylabel(r"$\chi^2$", fontsize=18)


s2s2 = []
Y_s2 = []
a2s = []
B_to_try = np.arange(5.0, 15.0, 0.01)
for baseline in B_to_try:
    a, Y_, s2, cov = fit_components(crab["ha"], crab.normed, #crab["volts"],
        lambda ha: np.cos(2*np.pi*(baseline/wl) * np.cos(catalog_dec) * np.sin(2.*np.pi*ha/24.)),
        lambda ha: - np.sin(2*np.pi*(baseline/wl) * np.cos(catalog_dec) * np.sin(2.*np.pi*ha/24.))
    )
    s2s2.append(s2)
    Y_s2.append(Y_)
    a2s.append(a)

a2 = a2s[np.argmin(s2s2)]
measured_B = B_to_try[np.argmin(s2s2)]
Y_ = Y_s2[np.argmin(s2s2)]

plt.figure()
plt.plot(B_to_try, s2s2, linewidth=2)
plt.xlabel(r"$B_y$ [m]", fontsize=18)
plt.ylabel(r"$\chi^2$", fontsize=18)

crab["volts"] = np.real(bandpass(2.0*np.pi*crab["t"]/86164., crab["volts"])[1])
plt.figure()
plt.subplot(211)
plt.plot(crab["ha"], crab["volts"])
plt.plot(crab["ha"], Y_, "k-", linewidth=2)
plt.xlabel(r"Hour angle [h]", fontsize=18)
plt.ylabel(r"Power", fontsize=18)
plt.subplot(212)
trans = np.fft.fft(crab["volts"])
freqs = np.fft.fftfreq(len(trans), 2.*np.pi * 1.0 / 86164.)
plt.plot(np.fft.fftshift(freqs), np.fft.fftshift(abs(trans)**2))
plt.xlabel(r"Frequency [rad$^{-1}$]", fontsize=18)
plt.ylabel(r"Power", fontsize=18)

