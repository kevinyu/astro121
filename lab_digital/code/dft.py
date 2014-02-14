import numpy as np


def dft(E, f_sample=1.0, power=True, f_res=None, f_max=None):
    """Do a discrete fourier transform on data array E

    E: data array
    f_sample (default=1.0): sample frequency of data
    power (default=True): return power spectrum if True
    f_res (default=None): resolution of power spectrum in Hz
        if None, uses f_sample/N

    >>> nu, Enu = dft(data, f_sample=1e3)
    >>> plot(nu, np.abs(Enu)**2)  # plots power spectrum
    """
    dt = (f_sample)**-1
    N = len(E)
    T = (N-1) * dt
    t_array = np.arange(-T/2., T/2. + dt, dt)

    def E_nu(nu):
        return sum(
            E_t * np.exp(2j*np.pi*nu*t) * dt
            for t, E_t in zip(t_array, E)
        ) / T

    if not f_max:
        f_res = f_res or f_sample / N
        nu = np.arange(-f_sample/2., (f_sample/2.) * (1. - 2./N) + f_sample/N, f_res)
    else:
        f_res = f_res or (f_max[1] - f_max[0]) / N
        nu = np.arange(-f_max, f_max, f_res)
    return (nu, abs(E_nu(nu)) ** 2) if power else (nu, E_nu(nu))
