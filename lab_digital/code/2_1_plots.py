from pylab import *
import numpy as np


f_sample = 10e6
dt = 1./f_sample

N = 16384
t = np.arange(0, N) * dt
data_p = np.load("../data/2_1_1/asdfasdffsig_840000.0.npz")["arr_0"]
data_m = np.load("../data/2_1_1/asdfasdffsig_760000.0.npz")["arr_0"]

plot(t, data_p)
figure()
plot(np.fft.fftfreq(N, dt), abs(np.fft.fft(data_p))**2)

figure()
plot(t, data_m)
figure()
plot(np.fft.fftfreq(N, dt), abs(np.fft.fft(data_m))**2)
