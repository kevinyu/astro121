from pylab import *

import os

from unfuckup import unfuckup
from fourier_filter import fourier_filter


# data from first trying to take data with the roach
test_dir = "../data/roach/redo22"

# now we redo the mixing from 2.1 except using the roach
dir_2_1_p = "../data/roach/mixing21p_new"
dir_2_1_m = "../data/roach/mixing21m_new"

# now we digitally mix!
digital_p = "../data/roach/digitalmixp"
digital_m = "../data/roach/digitalmixm"

# mix with LO
lomix = "../data/roach/lomix"


f_sample = 200e6

"""
#
data1 = np.fromfile(os.path.join(test_dir, "adc_bram"), dtype=">i")
t = np.arange(0, data1.size) / f_sample
figure()
plot(t, data1)

"""
#
'''
data2p = np.fromfile(os.path.join(dir_2_1_p, "adc_bram"), dtype=">i")
t = np.arange(0, data2p.size) / f_sample
figure()
plot(t, data2p)

figure()
output = np.fft.fft(data2p)
plot(np.fft.fftfreq(len(data2p), 1./f_sample), abs(output)**2, "kx")


data2m = np.fromfile(os.path.join(dir_2_1_m, "adc_bram"), dtype=">i")
t = np.arange(0, data2m.size) / f_sample
figure()
plot(t, data2m)

figure()
output = np.fft.fft(data2m)
plot(np.fft.fftfreq(len(data2m), 1./f_sample), abs(output)**2, "kx")
'''

'''
'''
figure()

#
digmixp = np.fromfile(os.path.join(digital_p, "mix_bram"), dtype=">i")
t = np.arange(0, digmixp.size) / f_sample
subplot(221)
plot(t*1e6, digmixp/1e3, "-", color="Orange")
title(r"$\nu_{sig} = 2.1 MHz$")
xlabel("Time ($\mu s$)", fontsize=14)
ylabel("V", fontsize=14)
xlim(0, 10)

output = np.fft.fft(digmixp)
subplot(212)
plot(1e-6 * unfuckup(np.fft.fftfreq(len(digmixp), 1./f_sample)), 1e-12 * unfuckup(abs(output)**2), color="Orange", linewidth=4)
xlabel("Frequency (MHz)", fontsize=14)
ylabel("Power", fontsize=14)
xlim(-6, 6)

digmixm = np.fromfile(os.path.join(digital_m, "mix_bram"), dtype=">i")
t = np.arange(0, digmixm.size) / f_sample
subplot(222)
plot(t*1e6, digmixm/1e3, "b-")
title(r"$\nu_{sig} = 1.9 MHz$")
xlabel("Time ($\mu s$)", fontsize=14)
gca().set_yticklabels([], visible=False)
xlim(0, 10)

output = np.fft.fft(digmixm)
subplot(212)
plot(1e-6*unfuckup(np.fft.fftfreq(len(digmixm), 1./f_sample)), 1e-12 * unfuckup(abs(output)**2), color="Blue", linewidth=2)
xlabel("Frequency (MHz)", fontsize=14)
ylabel("Power", fontsize=14)
xlim(-6, 6)
#
text(-5.3, 1, r"$-4.1 MHz$", fontsize=14)
text(-3.8, 1, r"$-3.9 MHz$", fontsize=14)
text(-1.3, 1.2, r"$-0.1 MHz$", fontsize=14)
text(.3, 1.2, r"$0.1 MHz$", fontsize=14)
text(2.9, 1, r"$3.9 MHz$", fontsize=14)
text(4.2, 1, r"$4.1 MHz$", fontsize=14)

blarg = [ylim()[0], ylim()[1] + .1]
plot([2, 2], blarg, "k--", label=r"$\pm \nu_{LO}$")
plot([-2, -2], blarg, "k--")
legend()
ylim(*blarg)


# let
lofreq = 4
mixfreq = 2e6 * lofreq / 256
datacos = np.fromfile(os.path.join(lomix + "-lo-%s" % lofreq, "cos_bram"), dtype=">i")
datasin = np.fromfile(os.path.join(lomix + "-lo-%s" % lofreq, "sin_bram"), dtype=">i")
full_wave = np.array(list(datacos[:]) +list(datacos[0:0])) - 1j * datasin

t = np.arange(0, datasin.size) / f_sample

figure()
subplot(211)
plot(t * 1e6, - 1e-6 * full_wave.imag, "-", color="Orange", alpha=.8, marker="None", linewidth=3, label=r"$-f_{sig}(t)\ \sin(\omega t)$")
plot(t * 1e6, 1e-6 * full_wave.real, "b-", alpha=.8, marker="None", linewidth=2, label=r"$f_{sig}(t)\ \cos(\omega t)$")

xlabel("Time ($\mu s$)", fontsize=14)
ylabel("V", fontsize=14)
xlim(4, 6)
subplot(212)
output = np.fft.fft(full_wave)
plot(1e-6 * unfuckup(np.fft.fftfreq(len(full_wave), 1./f_sample)), 1e-18 * unfuckup(abs(output)**2), "-")
LO_freq = lofreq / 256. * 200
ylim(1e-5, ylim()[1]*10)
bleh = ylim()
semilogy([0, 0], bleh, "k:")
text(-9, 1, r"$%.3f MHz$" % (-LO_freq - 6), fontsize=16)
text(-4, .1, r"$%.3f MHz$" % (-LO_freq), fontsize=16)
text(3, 1, r"$%.3f MHz$" % (-LO_freq + 6), fontsize=16)
ylim(*bleh)
# legend(loc=2, fontsize=14)
xlim(-15, 15)
xlabel("Frequency (MHz)", fontsize=14)
ylabel("Power", fontsize=14)

subplot(211)
tfilt, vfilt = fourier_filter(output, 200e6, kill_freqs=(-3.125e6, -9.125e6), kill_radius=5)
plot(tfilt * 1e6, 1e-6 * vfilt.real, "k-", linewidth=5, label="Re[Filtered]")
plot(tfilt * 1e6, 1e-6 * vfilt.imag, "k-", linewidth=5, alpha=0.5, label="Im[Filtered]")
xlim(3.9, 5.1)

legend(fontsize=14)
