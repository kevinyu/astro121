"""Process moon data"""

import numpy as np

import matplotlib.pyplot as plt

from fringe_funcs import fringe_freq, bessel
from lsq import fit_components
from utils import FourierFilter, Analyzer, find_roots


B = 10.06
wl = 3e8 / 10.67e9

datafile = "../data/moon-4_6_2014-24.npz"
logfile = "../data/logs/moon-4_6_2014-24-log"


moon = Analyzer(datafile, logfile, dt=1.0, start_at_timestamp="2014-04-06 20:33:14,728")

import ephem
import datetime
damoon = ephem.Moon()
obs = ephem.Observer()
obs.lat = np.deg2rad(37.8732)
obs.long = np.deg2rad(-122.2573)
obs.date = ephem.date("2014-04-06 20:12:45")
damoon.compute(obs)
for i, lst in enumerate(moon["lst"]):
    moon["ra"][i] = 24. * damoon.ra / (2. * np.pi)
    moon["dec"][i] = np.rad2deg(damoon.dec)
    obs.date += 1. / 86164.
    damoon.compute(obs)

moon.data["ha"] = moon.data["lst"] - moon.data["ra"]
moon.data["ha"] -= (24.0 * (moon.data["ha"] > 12.0))

moon.slice(0, len(moon["volts"])-5000)

# Next we set invalid points (from telescope homing) to the avg_dc
moon.flatten_invalid_points()

plt.subplot(211)
plt.plot(moon["ha"], moon["volts"])
plt.xlabel(r"Hour angle [h]", fontsize=18)
plt.ylabel(r"Power", fontsize=18)
plt.subplot(212)
trans = np.fft.fft(moon["volts"])
freqs = np.fft.fftfreq(len(trans), 2. * np.pi * 1.0 / 86164.)
plt.plot(np.fft.fftshift(freqs), np.fft.fftshift(abs(trans)**2))
plt.xlabel(r"Frequency [rad$^{-1}$]", fontsize=18)
plt.ylabel(r"Power", fontsize=18)

# Now we remove the dc offset, as well as high frequency noise
local_fringe_frequencies = fringe_freq(B, wl, moon["dec"], 2.*np.pi*moon["ha"]/24.)
bandpass = FourierFilter(min_freq=0.001, max_freq=max(local_fringe_frequencies))
# moon["volts"] = np.real(bandpass(moon["t"], moon["volts"])[1])
moon.flatten_invalid_points()
# moon["volts"] = moon.real_boxcar(200)
moon["volts"] = np.load("moonshine.npz")["volts"]

plt.figure()
plt.plot(moon["ha"], moon["volts"])
plt.xlabel(r"Hour angle [h]", fontsize=18)
plt.ylabel(r"Power", fontsize=18)
plt.plot(moon["ha"], moon.envelope(50))

'''
mooncopy = moon.copyslice(3600, 7100)
mooncopy["ha"] = mooncopy["ha"]

positive_values = mooncopy["volts"] >= 0.0
enveloper = FourierFilter(max_freq=0.01)
_, envelope = enveloper(mooncopy["t"], mooncopy["volts"] * positive_values)

phi_to_try = np.arange(0.0, np.pi, np.pi/300.)

s2s = []
Y_s = []
a_s = []

# a, Y_, s2, cov = fit_components(mooncopy["ha"], np.real(envelope),
for phi in phi_to_try:
    a, Y_, s2, cov = fit_components(mooncopy["ha"], mooncopy["volts"],
        lambda ha: F(ha, phi),
        lambda ha: F(ha, phi) * ha,
        lambda ha: F(ha, phi) * ha**2,
    )
    s2s.append(s2)
    Y_s.append(Y_)
    a_s.append(a)

C1, C2, C3 = a_s[np.argmin(s2s)]
Y_ = Y_s[np.argmin(s2s)]

print C1, C2, C3
ha1 = (-C2 + np.sqrt(C2**2. - 4*C1*C3)) / (2.*C3)
ha2 = (-C2 - np.sqrt(C2**2. - 4*C1*C3)) / (2.*C3)
print ha1
print ha2
'''

# Get theoretical MF values from bessel function
fR_range = np.arange(-2.0, 2.0, 0.0005)
bessel_y = bessel(fR_range)
expected_roots = np.array(find_roots(fR_range, bessel_y))

R_known = np.deg2rad(0.26)
expected_freqs = expected_roots / R_known


# plt.plot(moon["t"], moon["volts"])
minima_spots = [(7000, 11000)]
obs_zeros = []
plottypairs = []
for start, end in minima_spots:
    # Cut out a small window around the guessed envelope
    # fit a quadratic to find minima
    (C1, C2, C3), Y_, s2, cov = fit_components(moon["ha"][start: end], moon.envelope(50)[start:end],
        lambda ha: ha ** 2,
        lambda ha: ha,
        lambda ha: 1,
    )
    plottypairs.append((moon["ha"][start:end], Y_))
    vertex = -C2 / (2. * C1)
    obs_zeros.append(vertex)

    '''
    _, aa = zip(*sorted(zip(b, a)))
    min_ha = aa[0]
    obs_zeros.append(min_ha)

    print "found", min_ha
    plottypairs.append((a, b))
    '''
    print "found", vertex
obs_zeros = np.array(obs_zeros)

plt.plot(moon["ha"], moon.envelope(50))
for x, y in plottypairs:
    plt.plot(x, y)


index_of_zeros = np.array([moon["ha"].searchsorted(thing) for thing in obs_zeros])
obs_freqs = fringe_freq(B, wl, np.deg2rad(moon["dec"][index_of_zeros]), 2. * np.pi * obs_zeros / 24.)

print "obs_freqs =", obs_freqs




'''
demod = FourierFilter(max_freq=1.0)
# plt.plot(moon["ha"], abs(moon["volts"])/ max(moon["volts"]))
# a, b = demod(moon["ha"], abs(moon["volts"]))
# plt.plot(a, b / max(b))
# for x, y in plottypairs:
#    plt.plot(x, map(lambda x: x*100, y))

# Now we have the observed zero points obs_zeros
# Now to try different values of R
accuracy = 0.001  # Measure down to 0.1 of a degree
try_range = np.deg2rad(np.arange(0.262, 0.275, accuracy))  # try radii in this range

# We use the theoretical bessel function. which is a function
# of fringe frequnecy and R
# Since the bessel function is even, we can just find the zero crossings for positive hour angle, and then say they apply to negative as well
hour_zero_index = moon["ha"].searchsorted(0.0)
sliced = moon.copyslice(hour_zero_index, None)

# fringe frequency array
ffs = (10./0.025) * np.cos(np.deg2rad(sliced["dec"])) * np.cos(2*np.pi * sliced["ha"]  /24.)

bessels = []
for R in try_range:
    print "Bessling %s" % R
    bessels.append(bessel(ffs, R))

residual_squared = []
for besselout in bessels:
    zs = find_indexes_of_zero_crossings(besselout)[:2]
    zs = sliced["ha"][zs]
    if len(zs) < 2:
        residual_squared.append(100)
        continue
    zeros_for_this_R = np.array([-zs[1], -zs[0], zs[0], zs[1]])

    residual_squared.append(sum((obs_zeros - zeros_for_this_R)**2))
'''
