from pylab import *
import numpy as np

from dft import dft

t = np.arange(1e-5, 257e-5, 1e-5)


f, subplotaxes = plt.subplots(9, 2, sharex="col", sharey=False)
for x in range(1, 10):
    filedict = np.load("../data/1_1_1/fsig_%s.0.npz" % (x*1000))
    data = filedict["arr_0"]
    ax = subplotaxes[x-1][0]
    ax.set_title(r"$\nu_{sig}=%s kHz$" % x, rotation="horizontal")
    ax.plot(t*1e3, data, "-o")
    ax.set_xlim(0, 0.5)
    ax.set_yticklabels([], visible=False)

    f_sample = 10e3
    freq, data_fourier = dft(data, f_sample=f_sample, power=True)
    ax = subplotaxes[x-1][1]
    # ax.set_title(r"$\nu_{sig}=%s kHz$" % x)
    ax.plot(freq*1e-3, data_fourier)
    ax.set_yticklabels([], visible=False)
    ax.set_xlim(-6, 6)

subplotaxes[-1][0].set_xlabel("time (ms)")
subplotaxes[-1][1].set_xlabel("freq (kHz)")

# Fine-tune figure; make subplots close to each other and hide x ticks for
# all but bottom plot.
f.subplots_adjust(hspace=0)
# plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
