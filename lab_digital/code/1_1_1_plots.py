from pylab import *
import numpy as np
from scipy.optimize import curve_fit

from dft import dft

t = np.arange(1e-4, 257e-4, 1e-4)

t2 = np.arange(1e-4, 257e-4, 1e-6)

f, subplotaxes = plt.subplots(9, 2, sharex="col", sharey=False)
for x in range(1, 10):
    filedict = np.load("../data/1_1_1/fsig_%s.0.npz" % (x*1000))
    data = filedict["arr_0"]
    ax = subplotaxes[x-1][0]
    ax.set_ylabel(r"$\nu_{sig}=%s kHz$" % x, rotation="horizontal", fontsize=14)
    ax.plot(t*1e3, data, "-o", linewidth=2)

    # plot actual waveform lightly
    # first line them up
    fitfunc = lambda t, A, phi: A * np.cos(2*pi*x*1e3*t + phi)
    (A, phi), _ = curve_fit(fitfunc, t, data)
    ax.plot(t2*1e3, A*np.cos(2*pi*x*1e3*t2 + phi), "b-", alpha=0.2, linewidth=4)
    ax.set_xlim(0, 2.0)
    ax.set_ylim(-1.4, 1.4)
    ax.set_yticklabels([], visible=False)

    f_sample = 10e3
    freq, data_fourier = dft(data, f_sample=f_sample, power=True)
    ax = subplotaxes[x-1][1]
    # ax.set_title(r"$\nu_{sig}=%s kHz$" % x)
    ax.plot(freq*1e-3, data_fourier, linewidth=2)
    ax.set_yticklabels([], visible=False)
    ax.set_xlim(-6, 6)

subplotaxes[-1][0].set_xlabel("time (ms)", fontsize=14)
subplotaxes[-1][1].set_xlabel("freq (kHz)", fontsize=14)

# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
f.subplots_adjust(hspace=0)
# plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

# generate example of mixing
figure()
ax = gca()
x = 8
filedict = np.load("../data/1_1_1/fsig_%s.0.npz" % (x*1000))
data = filedict["arr_0"]
ax.plot(t*1e3-1e-1, data, "-o", markersize=12, color="Black", linewidth=2, label="Sampled Waveform")

# plot actual waveform lightly
# first line them up
fitfunc = lambda t, A, phi: A * np.cos(2*pi*x*1e3*t + phi)
(A, phi), _ = curve_fit(fitfunc, t, data)
ax.plot(t2*1e3-1e-1, A*np.cos(2*pi*x*1e3*t2 + phi), "b-", alpha=0.2, linewidth=4, label="Actual Signal")
ax.set_xlim(0, 1.0)
ax.set_ylim(-1.3, 1.3)
ax.set_xticklabels([], visible=False)
ax.set_yticklabels([], visible=False)
legend(loc="lower center", bbox_to_anchor=(0.5, -.1))
