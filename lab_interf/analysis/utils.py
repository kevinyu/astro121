"""
Utility functions
"""
import numpy as np

from clean_data import check_valid_points


class FourierFilter:
    def __init__(self, min_freq=0.0, max_freq=np.inf, kill_range=None):
        """Create a fourier filter

        min_freq (float, default=0.0):
            Filter out frequencies lower than this value
        max_freq (float, default=0.0):
            Filter out frequencies greater than this value
        """
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.kill_range = kill_range

    def keep_array(self, x_fourier):
        x_fourier = abs(x_fourier)
        return (x_fourier >= self.min_freq) * (x_fourier <= self.max_freq)

    def __call__(self, x_data, y_data):
        """Apply the filter to data

        x_data (np.array):
            Time array of dataset; make sure units make sense with min_freq/max_freq
        y_data (np.array):
            Blah

        Returns tuple of (x_data, filtered y_data)
        """
        dx = x_data[1] - x_data[0]
        y_fourier = np.fft.fft(y_data)
        x_fourier = np.fft.fftfreq(len(y_fourier), dx)

        filtered_y_fourier = y_fourier * self.keep_array(x_fourier)
        filtered_y_data = np.fft.ifft(filtered_y_fourier)

        return x_data, filtered_y_data


class Analyzer:
    def __init__(self, datafile, logfile, dt=None, ra=None, start_at_timestamp=None):
        self.dt = dt or 1.0
        # TODO: move check_valid_points into this class
        self.data = check_valid_points(np.load(datafile), logfile, start_at_timestamp=start_at_timestamp)
        self.data["t"] = np.arange(len(self.data["volts"])) * self.dt
        self.data["ha"] = self.data["lst"] - (ra or self.data["ra"])
        self.data["ha"] -= (24.0 * (self.data["ha"] > 12.0))

    def __getitem__(self, x):
        return self.data[x]

    def __setitem__(self, x, y):
        self.data[x] = y

    def keys(self):
        return self.data.keys()

    @staticmethod
    def load(filename):
        return dict(**np.load(filename))

    def set_dt(self, dt):
        self.dt = dt
        self.data["t"] = np.arange(len(self.data["volts"]))

    def copyslice(self, start, end):
        new_dict = dict((key, arr[start:end]) for key, arr in self.data.items())
        return new_dict

    def slice(self, start, end):
        for key in self.data.keys():
            self.data[key] = self.data[key][start:end]
        print "Sliced data from %s to %s" % (start, end)

    def flatten_invalid_points(self):
        avg_dc = np.mean(self["volts"])
        self["volts"] = (self["volts"] * self["valid"]) + (self.binned(600) * (self["valid"] == False))

    @property
    def normed(self):
        """ Normalize each chunk of 200 points to the maximum over that range """
        start = 0
        step = 200
        binned = np.array(self.data["volts"])
        while len(binned[start:start+step]):
            # med = np.max(abs(binned[start:start+step]))
            thebin = binned[start: start+step]
            med = np.median(thebin[thebin > 0.0])
            binned[start:start+step] = binned[start:start+step]
            start += step
        return binned

    def binned(self, step):
        """ Normalize each chunk of 200 points to the maximum over that range """
        start = 0
        medianed = np.zeros(len(self["volts"]))
        while len(medianed[start:start+step]):
            # med = np.max(abs(binned[start:start+step]))
            medianed[start:start+step] = np.median(abs(self["volts"][start:start+step]))
            start += step
        return medianed

    def boxcar(self, width):
        """ Normalize each chunk of 200 points to the maximum over that range """
        medianed = np.zeros(len(self["volts"]))
        for i, v in enumerate(self["volts"]):
            boxcar = self["volts"][self["valid"] == True][max(0, i-width/2.):min(len(self["volts"]), i+width/2.)]
            medianed[i] = v - np.median(boxcar)
        return medianed

    def real_boxcar(self, width):
        """ Normalize each chunk of 200 points to the maximum over that range """
        medianed = np.zeros(len(self["volts"]))
        for i, v in enumerate(self["volts"]):
            boxcar = list(self["volts"])[max(0, i-width/2):i+width/2]
            medianed[i] = np.median(boxcar)
        return self["volts"] - medianed

    def envelope(self, step):
        """ Normalize each chunk of 200 points to the maximum over that range """
        start = 0
        medianed = np.zeros(len(self["volts"]))
        while len(medianed[start:start+step]):
            # med = np.max(abs(binned[start:start+step]))
            medianed[start:start+step] = np.max(abs(self["volts"][start:start+step] - np.mean(self["volts"][start:start+step])))
            start += step
        return medianed



def find_roots(x, y):
    indicies = [i for i in range(len(y)-1) if (y[i] * y[i+1] < 0.0) or (y[i] == 0)]
    return [np.mean([x[i], x[i+1]]) for i in indicies]
