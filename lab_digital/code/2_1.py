import sys
import numpy as np

import DFEC


f_sample = 10e6  # 10 MHz
f_lo = 800e3  # 800 kHz
f_signal_p = 840e3  # 210 kHz
f_signal_m = 760e3  # 190 kHz


N = 16384
yes_array = ["y", "Y"]

for f_sig in [f_signal_p, f_signal_m]:
    go = raw_input("Safe to set srs?\n")
    if go not in yes_array:
        break
    DFEC.set_srs(1, freq=f_sig, dbm=0.0)
    DFEC.set_srs(2, freq=f_lo, dbm=0.0)
    go = raw_input("Check that SRS1 is outputting f=%s Hz\n and SRS2 is outputting f=%s Hz\n" % (
        f_sig, f_lo))
    if go not in yes_array:
        break
    data = DFEC.sampler(nSamp=N, freqSamp=f_sample)

    array_savefile = "../data/2_1_1/asdfasdffsig_%.1f.npz" % f_sig
    np.savez(array_savefile, data)
    print "Saved %s" % array_savefile
