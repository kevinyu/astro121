from pylab import *
import numpy as np

from fourier_filter import fourier_filter


f_sample = 10e6
dt = 1./f_sample

N = 16384
t = np.arange(0, N) * dt
data_p = np.load("../data/2_1_1/thurs_sig_2100000.0.npz")["arr_0"]
data_m = np.load("../data/2_1_1/thurs_sig_1900000.0.npz")["arr_0"]

figure(1)
subplot(121)
plot(t*1e6, data_p, "-", color="Orange")
xlabel(r"Time ($\mu s$)", fontsize=14)
ylabel("V", fontsize=14)
xlim(0, 20)
ylim(-.25, .25)
title(r"$\nu_{sig} = 2.1$ MHz")
figure(2)
subplot(211)
plot(np.fft.fftfreq(N, dt) * 1e-6, abs(np.fft.fft(data_p))**2 * 1e-6, color="Orange", linewidth=4, label=r"$\nu_{sig} = 2.1$ MHz")
ylabel("Power", fontsize=14)
gca().set_xticklabels([], visible=False)
plot([2, 2], [0, 0.9], "k--")
plot([-2, -2], [0, 0.9], "k--")
legend()

figure(1)
subplot(122)
plot(t*1e6, data_m, "b-")
xlabel(r"Time ($\mu s$)", fontsize=14)
title(r"$\nu_{sig} = 1.9$ MHz")
xlim(0, 20)
ylim(-.25, .25)
gca().set_yticklabels([], visible=False)

figure(2)
subplot(212)
plot(np.fft.fftfreq(N, dt) * 1e-6, abs(np.fft.fft(data_m))**2 * 1e-6, color="Blue", linewidth=2, label=r"$\nu_{sig} = 1.9$ MHz")
xlabel("Frequency (MHz)", fontsize=14)
ylabel("Power", fontsize=14)

plot([2, 2], [0, 0.9], "k--")
plot([-2, -2], [0, 0.9], "k--")
legend()

subplot(211)
text(-3.9, .4, r"$-4.1 MHz$", fontsize=14)
text(-1.3, .6, r"$-0.1 MHz$", fontsize=14)
text(.3, .6, r"$0.1 MHz$", fontsize=14)
text(2.9, .4, r"$4.1 MHz$", fontsize=14)

subplot(212)
text(-3.8, .4, r"$-3.9 MHz$", fontsize=14)
text(-1.3, .6, r"$-0.1 MHz$", fontsize=14)
text(.3, .6, r"$0.1 MHz$", fontsize=14)
text(2.9, .4, r"$3.9 MHz$", fontsize=14)
ylim(0, 0.9)

# now the fourier filtered waveform
figure(3)
subplot(121)
t, v = fourier_filter(np.fft.fft(data_p), 1./dt, kill_freqs=(4.1e6, -4.1e6), kill_radius=5)
plot(t*1e6, v, "-", color="Orange", linewidth=2)
xlabel(r"Time ($\mu s$)", fontsize=14)
ylabel("V", fontsize=14)
xlim(100, 120)
ylim(-.25, .25)

subplot(122)
t, v = fourier_filter(np.fft.fft(data_m), 1./dt, kill_freqs=(3.9e6, -3.9e6), kill_radius=5)
plot(t*1e6, v, "-", color="Blue", linewidth=2)
xlabel(r"Time ($\mu s$)", fontsize=14)
xlim(100, 120)
ylim(-.25, .25)
gca().set_yticklabels([], visible=False)
