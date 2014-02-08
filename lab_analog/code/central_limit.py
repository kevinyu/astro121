import random as random
import numpy as np

# Non-Normal Distributions Sampler
uniform = lambda: random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1)
dice = lambda: sum(random.sample([1, 2, 3, 4, 5, 6], 2))
blackjack= lambda: random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10], 1)
weird = lambda: random.sample([1, 1, 1, 1, 5, 9, 10, 25, 26, 30], 1)
gauss = lambda: random.gauss(0, 10)  # gaussian with mean 0 and std 1
randint = lambda: np.random.rand()


def collect_samples(distribution, n=5, N=10):
    sampled_means = []
    for i in np.arange(N):
        sampled = [distribution() for s in range(n)]
        sampled_means.append(np.mean(sampled))
    return sampled_means
