import numpy as np

def fourier_filter(power, df, kill_radius=6, kill_freqs=None):
    """Apply a fourier filter to a spectrum, returning filtered spectrum in time domain

    Applies a fourier filter to "power" array, originally taken with sample rate df,
    by killing peaks at the frequencies specified by *kill_freqs and the surrounding "kill_radius" points
    power argument should be ordered in the same way that np.fft.fft would output

    Returns the time domain waveform by reverse fourier transforming the filtered
    power spectrum."""
    if not kill_freqs:
        raise Exception("Must specify kill_freqs as a list of frequnecies")

    dt = 1./df
    df = df/len(power)

    for freq in kill_freqs:
        idx = int(freq / df)
        print power[idx-9: idx+9]
        power[idx] = 0.0
        for i in range(1, kill_radius):
            power[idx-i % len(power)] = 0.0
            power[idx+i % len(power)] = 0.0
        print power[idx-9: idx+9]

    v = np.fft.ifft(power)
    t = np.arange(len(power)) * dt
    return t, v
