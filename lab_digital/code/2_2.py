import os
import sys
import numpy as np

import DFEC

'''
f_lo = 800e3  # 800 kHz
f_signal_p = 840e3  # 210 kHz
f_signal_m = 760e3  # 190 kHz
'''

f_lo = 2e6  # 2 MHz
f_signal_p = 2.1e6  # 2.1 MHz
f_signal_m = 1.9e6  # 1.9 MHz

yes_array = ["y", "Y"]


if raw_input("Collect data for 2_1 digitally?"):
    for f_sig in [f_signal_p, f_signal_m]:
        go = raw_input("Safe to set srs?\n")
        if go not in yes_array:
            break
        # DFEC.set_srs(1, freq=f_sig, dbm=-10.0)
        # DFEC.set_srs(2, freq=f_lo, dbm=-10.0)
        go = raw_input("Check that SRS1 is outputting f=%s Hz\n and SRS2 is outputting f=%s Hz\n" % (
            f_sig, f_lo))
        if go not in yes_array:
            break

        # sample from roach
        # ran roach_heist with what directory name?
        
        PID = raw_input("Trigger data collection now. PID of .bof on roach?\n")
        name_of_directory = raw_input("Name the data directory for the data to go into: ")
        os.system("./roach_heist %s %s" % (PID, name_of_directory))

        print "Saved roach data in /home/kyu/astro121/lab_digital/data/roach/%s" % name_of_directory


if raw_input("Do digital mixing shiznit?"):
    for f_sig in [f_signal_p, f_signal_m]:
        go = raw_input("Safe to set srs?\n")
        if go not in yes_array:
            break
        # DFEC.set_srs(1, freq=f_sig, dbm=-10.0)
        # DFEC.set_srs(2, freq=f_lo, dbm=-10.0)
        go = raw_input("Check that SRS1 is outputting f=%s Hz\n and SRS2 is outputting f=%s Hz\n" % (
            f_sig, f_lo))
        if go not in yes_array:
            break

        # sample from roach
        # ran roach_heist with what directory name?
        
        PID = raw_input("Trigger data collection now. PID of .bof on roach?\n")
        name_of_directory = raw_input("Name the data directory for the data to go into: ")
        os.system("./roach_heist %s %s" % (PID, name_of_directory))

        print "Saved roach data in /home/kyu/astro121/lab_digital/data/roach/%s" % name_of_directory



if raw_input("Collect data for LO mixing?"):
    go = raw_input("Safe to set srs?\n")
    if go not in yes_array:
        sys.exit(1)
    # DFEC.set_srs(2, freq=1e6, dbm=-10.0)
    go = raw_input("Check that SRS2 is outputting f=%s Hz\n" % (2e6))
    if go not in yes_array:
        sys.exit(1)
    # sample from roach
    # ran roach_heist with what directory name?
    for lo_freq in [1, 2, 4, 16]:
        PID = raw_input("Write a %s to lo_freq to mix with %s MHz signal. Trigger data collection now. PID of .bof on roach?\n" % (lo_freq, 200. * lo_freq/256.))
        name_of_directory = raw_input("Name the data directory for the data to go into: ")
        os.system("./roach_heist %s %s-lo-%s" % (PID, name_of_directory, lo_freq))

        print "Saved roach data in /home/kyu/astro121/lab_digital/data/roach/%s" % name_of_directory

