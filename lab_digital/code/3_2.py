import os
import sys
import numpy as np


f_sample = 200e6
f_signal = 25e6

# lo_freqs = [4, 16, 32, 64]
lo_freqs = [4, 16, 32, 64]
lo_freqs = [40, 46, 48, 50, 56]

yes_array = ["y", "Y"]


'''
# collect unfiltered sine wave
raw_input("Set all coefficients to 0 except set one to close to 1.\n")
PID = raw_input("Trigger data collection now. PID of .bof on roach?\n")
name_of_directory = raw_input("Name the data directory for the data to go into: ")
os.system("./roach_heist %s %s" % (PID, name_of_directory))

print "Saved roach data in /home/kyu/astro121/lab_digital/data/roach/%s" % name_of_directory
'''
# now do the different LO frequencies
go = raw_input("Set all coeffs now.\n")
for lo_freq in lo_freqs:
    raw_input("Set lo_freq to %s and trigger data collection\n" % lo_freq)

    PID = raw_input("Trigger data collection now. PID of .bof on roach?\n")
    name_of_directory = raw_input("Name the data directory for the data to go into: ")
    os.system("./roach_heist %s %s-lo-%s" % (PID, name_of_directory, lo_freq))

    print "Saved roach data in /home/kyu/astro121/lab_digital/data/roach/%s" % name_of_directory

