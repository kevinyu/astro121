import sys


process = sys.argv[1]

trig_file = "/proc/{PID}/hw/ioreg".format(PID=process)

with open(trig_file, "wb") as trig:
    trig.write("\x00\x00\x00\x01")  # Not sure why but this writes 0000 0001
    trig.write("\x00\x00\x00\x00")
