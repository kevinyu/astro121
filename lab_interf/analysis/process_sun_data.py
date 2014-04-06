"""Process sun data"""

import numpy as np

import matplotlib.pyplot as plt

from utils import FourierFilter, Analyzer, bessel, find_indexes_of_zero_crossings


datafile = "../data/sun-4_3_2014-22.npz"
logfile = "../data/logs/sun-4_3_2014-22-log"

sun = Analyzer(datafile, logfile, dt=1.0)

# First we will remove that raised section at the end (starts at index 26000)
sun.slice(0, 26000)

# Next we set invalid points (from telescope homing) to the avg_dc
sun.flatten_invalid_points()

# Now we remove the dc offset, as well as high frequency noise
bandpass = FourierFilter(min_freq=0.001, max_freq=0.032)
sun["volts"] = np.real(bandpass(sun["t"], sun["volts"])[1])

minima_guesses = [-3.13, -2.22, 2.35, 3.2]
obs_zeros = []
plottypairs = []
for guess in minima_guesses:
    # For each minima in the bessel-like envelope:
    # Cut out a small window around the guessed envelope
    # Fourier filter the higher frequencies out to get envelope
    # Minimum of result is new guess for minima.
    # Cut out a smaller window around this new guess
    # apply the same procedure x amount of times until guess is
    # satisfactory
    demod = FourierFilter(max_freq=5.0)
    guess_index = sun["ha"].searchsorted(guess)
    sliced = sun.copyslice(guess_index-500, guess_index+500)
    a, b = demod(sliced["ha"], abs(sliced["volts"]))
    _, aa = zip(*sorted(zip(b, a)))
    min_ha = aa[0]
    obs_zeros.append(min_ha)

    print "found", min_ha
    plottypairs.append((a, b))
obs_zeros = np.array(obs_zeros)

demod = FourierFilter(max_freq=1.0)
# plt.plot(sun["ha"], abs(sun["volts"])/ max(sun["volts"]))
# a, b = demod(sun["ha"], abs(sun["volts"]))
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
hour_zero_index = sun["ha"].searchsorted(0.0)
sliced = sun.copyslice(hour_zero_index, None)

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
