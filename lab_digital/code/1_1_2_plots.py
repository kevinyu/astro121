from pylab import *
import numpy as np

from dft import dft


t = np.arange(1e-5, 257e-5, 1e-5)

# f_signal = f_nu
filedict = np.load("../data/1_1_2/f_10000Hz.npz")
data = filedict["arr_0"]
title(r"$\nu_{sig}=\nu_{samp}=10 kHz$")
plot(t, data)
xlim(0, 0.0005)
ylim(-1, 1)

figure()
# f_signal >> f_sample
subplot(211)
filedict = np.load("../data/1_1_2/fast_signal.npz")
data = filedict["arr_0"]
title(r"$\nu_{sig}=10MHz,\nu_{samp}=7kHz$")
plot(t, data)

# TODO plot an acutal 10MHz wave on top of this

subplot(212)
f_sample = 7e3
freq, data_fourier = dft(data, f_sample=f_sample, power=True, f_max=10e3, f_res=1.)
title(r"$\nu_{sig}=10MHz,\nu_{samp}=7kHz$")
plot(freq, data_fourier)

# TODO plot actual foureir transform of 10MHZ sine wave on top of this
