from pylab import *

from unfuckup import unfuckup


datapoints = []
threshold = 1e17  # if a point is higher than this in the unfiltered power specturm, take it as a datapoint
for x in [4, 16, 32, 40, 46, 48, 50, 56, 64]:
    norm_real = np.fromfile("../data/roach/norm-lo-%s/ddc_real_bram" % x, ">i")
    norm_imag = np.fromfile("../data/roach/norm-lo-%s/ddc_imag_bram" % x, ">i")
    actual_real = np.fromfile("../data/roach/FIR-lo-%s/ddc_real_bram" % x, ">i")
    actual_imag = np.fromfile("../data/roach/FIR-lo-%s/ddc_imag_bram" % x, ">i")
    norm = norm_real + 1j * norm_imag
    actual = actual_real + 1j * actual_imag
    norm_fft = abs(np.fft.fft(norm))**2
    actual_fft = abs(np.fft.fft(actual))**2

    for i, freq in enumerate(np.fft.fftfreq(len(norm_fft), 1/200e6)):
        if norm_fft[i] > threshold:
            datapoints.append([freq, actual_fft[i]/norm_fft[i], actual_fft[i], norm_fft[i]])
    # plot(unfuckup(abs(norm_fft)**2))
    # plot(unfuckup(abs(actual_fft)**2))
    # plot(unfuckup(abs(actual_fft)**2 / abs(norm_fft)**2))

    # now the negative side; i.e. mixing with a negative frequency
    norm = norm_real - 1j * norm_imag
    actual = actual_real - 1j * actual_imag
    norm_fft = abs(np.fft.fft(norm))**2
    actual_fft = abs(np.fft.fft(actual))**2

    for i, freq in enumerate(np.fft.fftfreq(len(norm_fft), 1/200e6)):
        if norm_fft[i] > threshold:
            datapoints.append([freq, actual_fft[i]/norm_fft[i], actual_fft[i], norm_fft[i]])

data = np.array(datapoints)

# plot(data[:, 0]*1e-6, data[:, 1], "o", markersize=8)
# xlabel("Frequency (MHz)", fontsize=16)
# ylabel(r"$P_{filtered}/P_{unfiltered}$", fontsize=16)
