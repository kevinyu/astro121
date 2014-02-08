from pylab import *
import numpy as np

from impedances import C, CircuitImpedance, L, R, VoltageDivider


def capacitor_v_divider():
    """1.2.2 Capacitor voltage divider"""
    f = np.arange(1, 10000)
    C1, R1 = C(1e-6), R(1e3)
    RC = CircuitImpedance([R1, C1])
    divider = VoltageDivider(C1, RC)
    semilogx(f, divider.response(2*pi*f), "b-", linewidth=2)
    ylabel(r"$V_{out}/V_{in}$", fontsize=18)
    xlabel(r"$f$ $(Hz)$", fontsize=18)
    xticks(fontsize=14)
    yticks(fontsize=14)
    show()


def RC_filters():
    """1.3.1 RC filters expected responses"""
    f = np.arange(1e4, 1e6, 1e2)
    C1, R1 = C(1e-6), R(1.6)
    highpass = VoltageDivider(C1, R1)
    lowpass = VoltageDivider(R1, C1)
    semilogx(f, highpass.response(2*pi*f), "b-", linewidth=2, label="High-pass filter")
    semilogx(f, lowpass.response(2*pi*f), "r-", linewidth=2, label="Low-pass filter")
    ylabel(r"$V_{out}/V_{in}$", fontsize=18)
    xlabel(r"$f$ $(Hz)$", fontsize=18)
    xticks(fontsize=14)
    yticks(fontsize=14)
    legend(loc=3)
    show()


def LC_impedance_v_freq():
    """1.4.2 LC Impedance vs Frequency plot for L and C in parallel and in series"""
    f = np.logspace(4, 7, num=20000)  # the more resolution at resonance, better the peaks
    C1, L1 = C(1e-6), L(1e-6)
    parallel = CircuitImpedance([L1, C1])
    series = CircuitImpedance([L1], [C1])
    loglog(f, abs(parallel.Z(2*pi*f)), "m-", linewidth=2, label="C and L in parallel")
    loglog(f, abs(series.Z(2*pi*f)), "c-", linewidth=2, label="C and L in series")
    ylabel(r"Impedance $(\Omega)$", fontsize=18)
    xlabel(r"$f$ $(Hz)$", fontsize=18)
    xticks(fontsize=14)
    yticks(fontsize=14)
    ylim(1e-3, 1e3)
    legend(loc=1)
    show()


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
    ylabel(r"$P_{out}/P_{in}$", fontsize=18)
    plot([1.045e6, 1.045e6], ylim(), "r--", label=r"$1.045 MHz$", linewidth=2)
    plot([1.045e6-100e3, 1.045e6-100e3], ylim(), "r:", label=r"$\pm100 kHz$", linewidth=2)
    plot([1.045e6+100e3, 1.045e6+100e3], ylim(), "r:", linewidth=2)
    xlabel(r"$f$ $(Hz)$", fontsize=18)
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
    ylabel(r"$V_{out}/V_{in}$", fontsize=18)
    plot([1.045e6, 1.045e6], ylim(), "r--", linewidth=2, label=r"FM Carrier $1.045 MHz$")
    plot([20, 20], ylim(), "g:", linewidth=2, label=r"Audible $(20Hz-20kHz)$")
    plot([20e3, 20e3], ylim(), "g:", linewidth=2)
    xlabel(r"$f$ $(Hz)$", fontsize=18)
    xticks(fontsize=14)
    yticks(fontsize=14)
    # ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
    legend(loc=3)
    show()
