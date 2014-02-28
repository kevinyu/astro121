from pylab import *

import os


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

#
digmixp = np.fromfile(os.path.join(digital_p, "mix_bram"), dtype=">i")
t = np.arange(0, digmixp.size) / f_sample
figure()
plot(t, digmixp)

figure()
output = np.fft.fft(digmixp)
plot(np.fft.fftfreq(len(digmixp), 1./f_sample), abs(output)**2, "kx")

digmixm = np.fromfile(os.path.join(digital_m, "mix_bram"), dtype=">i")
t = np.arange(0, digmixm.size) / f_sample
figure()
plot(t, digmixm)

figure()
output = np.fft.fft(digmixm)
plot(np.fft.fftfreq(len(digmixm), 1./f_sample), abs(output)**2, "kx")
'''
#

# let
lofreq = 4
mixfreq = 2e6 * lofreq / 256
datacos = np.fromfile(os.path.join(lomix + "-lo-%s" % lofreq, "cos_bram"), dtype=">i")
datasin = np.fromfile(os.path.join(lomix + "-lo-%s" % lofreq, "sin_bram"), dtype=">i")
full_wave = datacos + 1j * datasin

t = np.arange(0, datasin.size) / f_sample

figure()
plot(t, full_wave.real, "b-", marker="x")
plot(t, full_wave.imag, "r-", marker="x")
figure()
output = np.fft.fft(full_wave)
plot(np.fft.fftfreq(len(full_wave), 1./f_sample), abs(output)**2)
