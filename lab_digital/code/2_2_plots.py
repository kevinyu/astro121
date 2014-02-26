from pylab import *

import os


# data from first trying to take data with the roach 
test_dir = "../data/roach/redo22"

# now we redo the mixing from 2.1 except using the roach
dir_2_1_p = "../data/roach/mixing21p"
dir_2_1_m = "../data/roach/mixing21m"

# now we digitally mix!
digital_p = "../data/roach/mixing21p"
digital_m = "../data/roach/mixing21m"

# mix with LO
lomix = "../data/roach/lomix"


f_sample = 200e6

# 
data1 = np.fromfile(os.path.join(test_dir, "adc_bram"), dtype=">i")
t = np.arange(0, data1.size) / f_sample
figure()
plot(t, data1)

"""
#
data2p = np.fromfile(os.path.join(dir_2_1_p, "adc_bram"), dtype=">i")
t = np.arange(0, data2p.size) / f_sample
figure()
plot(t, data2p)

data2m = np.fromfile(os.path.join(dir_2_1_m, "adc_bram"), dtype=">i")
t = np.arange(0, data2m.size) / f_sample
figure()
plot(t, data2m)

#
data2p = np.fromfile(os.path.join(digitalp, "mix_bram"), dtype=">i")
t = np.arange(0, data2p.size) / f_sample
figure()
plot(t, data2p)

data2m = np.fromfile(os.path.join(digitalm, "mix_bram"), dtype=">i")
t = np.arange(0, data2m.size) / f_sample
figure()
plot(t, data2m)

"""
#
datacos = np.fromfile(os.path.join(lomix, "cos_bram"), dtype=">i")
t = np.arange(0, datacos.size) / f_sample
figure()
plot(t, datacos)

datasin = np.fromfile(os.path.join(lomix, "sin_bram"), dtype=">i")
t = np.arange(0, datasin.size) / f_sample
figure()
plot(t, datasin)
