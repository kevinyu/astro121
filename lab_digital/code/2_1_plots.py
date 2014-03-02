from pylab import *
import numpy as np


f_sample = 10e6
dt = 1./f_sample

N = 16384
t = np.arange(0, N) * dt
data_p = np.load("../data/2_1_1/thurs_sig_2100000.0.npz")["arr_0"]
data_m = np.load("../data/2_1_1/thurs_sig_1900000.0.npz")["arr_0"]

subplot(221)
plot(t*1e6, data_p, "-", color="Orange")
xlabel(r"time ($\mu s$)", fontsize=14)
ylabel("amplitude", fontsize=14)
xlim(0, 20)
title(r"$\nu_{sig} = 2.1 MHz$")
subplot(212)
plot(np.fft.fftfreq(N, dt) * 1e-6, abs(np.fft.fft(data_p))**2 * 1e-6, color="Orange", linewidth=4)
xlabel("frequency (MHz)", fontsize=14)
ylabel("power", fontsize=14)

subplot(222)
plot(t*1e6, data_m, "b-")
xlabel(r"time ($\mu s$)", fontsize=14)
title(r"$\nu_{sig} = 1.9 MHz$")
xlim(0, 20)
gca().set_yticklabels([], visible=False)
subplot(212)
plot(np.fft.fftfreq(N, dt) * 1e-6, abs(np.fft.fft(data_m))**2 * 1e-6, color="Blue", linewidth=2)
xlabel("frequency (MHz)", fontsize=14)
ylabel("power", fontsize=14)

plot([2, 2], [0, 0.9], "k--", label=r"$\pm \nu_{LO}$")
plot([-2, -2], [0, 0.9], "k--")
legend()

text(-5.3, .4, r"$-4.1 MHz$", fontsize=12)
text(-3.8, .4, r"$-3.9 MHz$", fontsize=12)
text(-1.3, .6, r"$-0.1 MHz$", fontsize=12)
text(.3, .6, r"$0.1 MHz$", fontsize=12)
text(2.9, .4, r"$3.9 MHz$", fontsize=12)
text(4.2, .4, r"$4.1 MHz$", fontsize=12)
ylim(0, 0.9)
