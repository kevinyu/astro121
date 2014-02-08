from pylab import *
import numpy as np

from impedances import C, CircuitImpedance, L, R, VoltageDivider


def bandpass_plot():
    """1.7 Bandpass plot for our actual FM reciever values"""
    f = np.arange(100000, 10000000, 1000)
    L1, C1, R1 = L(1e-6), C(10e-9), R(27.)
    Resistors = CircuitImpedance([R1, R1])
    LC_loop = CircuitImpedance([L1, C1, C1, C1])
    bandpass = VoltageDivider(Resistors, LC_loop)
    plot(f, bandpass.response(2*pi*f)**2, "b-", linewidth=2)
    # format plot with slightly weird bounds for aesthetic reasons
    xlim(680000, 1320000)
    ylim(ylim()[0], ylim()[1] + .05)
    # plot(xlim(), [.5, .5], "m-", label="half power")
    ylabel(r"$P_{out}/P_{in}$", fontsize=14)
    plot([1.045e6, 1.045e6], ylim(), "r--", label=r"$1.045 MHz$", linewidth=2)
    plot([1.045e6-100e3, 1.045e6-100e3], ylim(), "r:", label=r"$\pm100 kHz$", linewidth=2)
    plot([1.045e6+100e3, 1.045e6+100e3], ylim(), "r:", linewidth=2)
    xlabel(r"$f$ $(Hz)$", fontsize=14)
    xticks(fontsize=14)
    yticks(fontsize=14)
    ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
    legend(loc=3)
    show()

def final_lowpass():
    """1.7 Bandpass plot for low pass at end of FM reciever"""
    f = np.arange(10, 1e9, 1e4)
    C1, R1 = C(1e-9), R(1e3)
    lowpass = VoltageDivider(R1, C1)
    semilogx(f, lowpass.response(2*pi*f), "b-", linewidth=2)
    ylabel(r"$V_{out}/V_{in}$", fontsize=14)
    plot([1.045e6, 1.045e6], ylim(), "r--", linewidth=2, label=r"FM Carrier $1.045 MHz$")
    plot([20, 20], ylim(), "g:", linewidth=2, label=r"Audible $(20Hz-20kHz)$")
    plot([20e3, 20e3], ylim(), "g:", linewidth=2)
    xlabel(r"$f$ $(Hz)$", fontsize=14)
    xticks(fontsize=14)
    yticks(fontsize=14)
    # ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
    legend(loc=3)
    show()
