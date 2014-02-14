import sys
import numpy as np

import DFEC


# disable DFEC for testing
def empty_func(*args, **kwargs):
    print args, kwargs
# DFEC.set_srs = empty_func
# DFEC.sampler = empty_func


# provide arguments on command line
# $ python 1_1_1.py 256 1e3

N, f_sample = sys.argv[1:]
N = int(N)
f_sample = float(f_sample)


yes_array = ["y", "Y"]
for x in np.arange(0.1, 1.0, 0.1):
    f_signal = x * f_sample
    go = raw_input("Safe to set srs?\n")
    if go not in yes_array:
        break
    DFEC.set_srs(1, freq=f_signal, vpp=1.0)
    go = raw_input("Check that LO 1 is outputting f=%s Hz\n" % f_signal)
    if go not in yes_array:
        break
    data = DFEC.sampler(nSamp=N, freqSamp=f_sample)

    array_savefile = "../data/1_1_1/fsig_%.1f.npz" % f_signal
    np.savez(array_savefile, data)
    print "Saved %s" % array_savefile
