from pylab import *
import numpy as np


t = np.arange(1e-5, 257e-5, 1e-5)
for x in range(1, 10):
    filedict = np.load("../data/1_1_1/fsig_%s.0.npz" % (x*1000))
    data = filedict["arr_0"]
    subplot(9, 2, x * 2 - 1)
    title("%s Hz" % (x * 1000))
    plot(t, data)
    
    data_fft = np.fft.fft(data)
    subplot(9, 2, (x * 2))
    title("%s Hz" % (x * 1000))
    plot(np.fft.fftfreq(256) * 10e3, data_fft)
