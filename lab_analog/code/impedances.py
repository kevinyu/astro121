import numpy as np


class R(object):
    def __init__(self, resistance):
        self.value = float(resistance)  # ohms

    def Z(self, w=1.e3):
        """Resistor with impdance of R (resistance in Ohms)"""
        return self.value


class C(object):
    def __init__(self, capacitance):
        """Capacitor with impedance of (1j*w*C)**-1 (capacitance in Farads)

        >>> C1 = C(1e-6)
        >>> C1.Z(w=2*pi*1e6)
        6.283185307179585j
        >>> abs(L1.Z(w=2*pi*1e6))
        6.283185307179585
        """
        self.value = float(capacitance)  # farads

    def Z(self, w=1.e3):
        """The impedance of the capacitor for frequency w"""
        if w == 0.0:
            return np.inf
        return (1j*w*self.value)**-1


class L(object):
    def __init__(self, inductance):
        """Inductor with impdeance of 1j*w*L (inductance in Henries)

        >>> L1 = L(1e-6)
        >>> L1.Z(w=2*pi*1e6)
        6.283185307179585j
        >>> abs(L1.Z(w=2*pi*1e6))
        6.283185307179585
        """
        self.value = float(inductance)  # henries

    def Z(self, w=1.e3):
        """The impedance of the inductor for frequency w"""
        return 1j*w*self.value


class CircuitImpedance(object):
    def __init__(self, *parallel_groups):
        """Create an equivalent impedance for multiple connected components

        Each argument should be a list of parallel components connected in series

        >>> L1, C1, R1 = L(1e-6), C(1e-6), R(1e3)
        >>> circuit = CircuitImpedance([R1], [L1, C1])
        >>> circuit.Z(1.5e6)
        1000-1.2j
        >>> circuit.Z(1e6)
        inf
        """
        self.components = parallel_groups

    def _parallel_Z_eq(self, components, w):
        Zs = np.array([component.Z(w) for component in components])
        if 0.0 in Zs:
            return 0.0
        else:
            total = sum(Zs**-1)
            if total == 0.0:
                return np.inf
            return total**-1

    def Z(self, w=1.e3):
        return sum([self._parallel_Z_eq(parallel_components, w) for parallel_components in self.components])


class VoltageDivider(object):
    def __init__(self, R1, R2):
        """An object for calculating response of a voltage divider

        Takes an object with (complex) impdance R1 connected from input to the output,
        and an object with (complex) impdance R2 connected from output to ground

        >>> L1, C1, R1 = L(1e-6), C(1e-6), R(1e3)
        >>> LC_loop = CircuitImpedance([L1, C1])
        >>> divider = VoltageDivider(R1, LC_loop)  # a LC bandpass filter
        >>> divider.response(1e6)
        1.0
        >>> divider.response(1.1e6)
        0.0011999991360009332
        """
        self.R1 = R1
        self.R2 = R2

    def _response(self, w):
        if self.R1.Z(w) == np.inf:
            raise Exception("This is an exceptional case and most likely you did something horrible.")
        if self.R2.Z(w) == np.inf:
            return 1.0
        return abs((self.R2.Z(w) / (self.R2.Z(w) + self.R1.Z(w))))

    def response(self, w):
        """Returns the response (V_out/V_in) of the voltage divider at frequency w."""
        try:
            iter(w)
        except:
            # if its not an iterable, just return _response
            return self._response(w)
        else:
            # if it is an iterable, map _response to each element to deal with the inf cases
            return np.array(map(self._response, w))
