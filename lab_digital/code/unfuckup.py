import numpy as np

def unfuckup(fftoutput):
    """Unfuckups the order of stuff so i can plot it without the stupid line going across"""
    half = len(fftoutput)/2
    return np.array(list(fftoutput[half:]) + list(fftoutput[:half]))
