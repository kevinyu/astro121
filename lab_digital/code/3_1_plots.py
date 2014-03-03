# Ideal 5/8-band filter vs FIR (frequency)
from pylab import *

from unfuckup import unfuckup

ideal_f = np.array(range(150) + range(-150, 0))
discrete_f = np.array(range(0, 100, 25) + range(-100, 0, 25))

bandpass = lambda x: abs(x) <= 62.5

ideal_r = bandpass(ideal_f)
discrete_r = bandpass(discrete_f)

figure(1)
plot([0,0], [-.5, 2.0], "k:")
plot([-150,150], [0,0], "k:")

plot(unfuckup(ideal_f), unfuckup(ideal_r), "b-", linewidth=3, label="Ideal Bandpass")
xlim(-150, 150)
ylim(-.04, 2.0)
xlabel("Frequency (MHz)")
ylabel("Response")

discrete_transform = np.fft.ifft(discrete_r)
discrete_t = np.array(range(4) + range(-4, 0)) * 5

figure(2)
plot([0,0], [-.5, 2.0], "k:")
plot([-150,150], [0,0], "k:")
plot(discrete_t, discrete_transform.real, "rs", markersize=8, label="Time Domain Coefficients")
xlim(-20, 20)
ylim(-.2, .7)
xlabel("t (ns)")
ylabel("Value")

figure(1)
padded_transform = np.array([0] * 60 + list(discrete_transform[4:]) + list(discrete_transform[:4]) + [0] * 60)
padded_t = np.array(range(64) + range(-64, 0)) * 5

actual_filter = np.fft.fft(padded_transform)
plot(unfuckup(discrete_f), unfuckup(discrete_r), "rs", markersize=8, label="Discrete Bandpass")
plot(unfuckup(np.fft.fftfreq(len(actual_filter), 1/200.)), unfuckup(abs(actual_filter)**2), "r--", linewidth=2, label="Predicted Response")


legend()


# now a figure just of predicted response and actual response
figure(3)
plot([0,0], [-.5, 2.0], "k:")
plot([-150,150], [0,0], "k:")
xlim(-150, 150)
ylim(-.04, 1.8)
xlabel("Frequency (MHz)", fontsize=16)
ylabel("Response", fontsize=16)
plot(unfuckup(ideal_f), unfuckup(ideal_r), "b-", linewidth=4, alpha=.2, label="Ideal Bandpass")
plot(unfuckup(np.fft.fftfreq(len(actual_filter), 1/200.)), unfuckup(abs(actual_filter)**2), "r--", linewidth=4, label=r"Predicted Response")

from test_fir import data
plot(data[:, 0]*1e-6, data[:, 1], "o", markersize=8, label=r"Actual Response: $P_{filtered}/P_{unfiltered}$")
legend()
# xlabel("Frequency (MHz)", fontsize=16)
# ylabel(, fontsize=16)
