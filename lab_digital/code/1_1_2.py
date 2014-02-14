import numpy as np

import DFEC 


# 1.1.2 f_signal = f_sample
def equal_frequency():
    f_signal = 10e3
    f_sample = 10e3

    yes_array = ["y", "Y"]

    DFEC.set_srs(1, freq=f_signal, vpp=1.0)
    go = raw_input("Check that LO 1 is outputting f=%s Hz\n" % f_signal)
    if go in yes_array:
        data = DFEC.sampler(nSamp=256, freqSamp=f_sample)
        np.savez("../data/1_1_2/f_10000Hz.npz", data)

# 1.1.2 f_signal >> f_sample
def slow_sample_rate():
    f_signal = 10e6
    f_sample = 7e3

    yes_array = ["y", "Y"]

    DFEC.set_srs(1, freq=f_signal, vpp=1.0)
    go = raw_input("Check that LO 1 is outputting f=%s Hz\n" % f_signal)
    if go in yes_array:
        data = DFEC.sampler(nSamp=256, freqSamp=f_sample)
        np.savez("../data/1_1_2/fast_signal.npz", data)
