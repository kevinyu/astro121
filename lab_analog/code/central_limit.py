import random as r
import numpy as np
from pylab import *
from scipy.stats import norm
from scipy.optimize import curve_fit


# Distributions
uniform = lambda: r.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1)
dice = lambda: sum(r.sample([1, 2, 3, 4, 5, 6], 2))
def blackjack():
    x, y = r.sample([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4, 2)
    return x + y - (10 if ((x + y) > 21 and 11 in (x, y)) else 0)
weird = lambda: r.sample([1, 1, 1, 1, 5, 9, 10, 25, 26, 30], 1)
gauss = lambda: r.gauss(0, 10)  # gaussian with mean 0 and std 1
randnumber = lambda: np.random.rand()


def collect_samples(distribution, n=5, N=10):
    sampled_means = []
    for i in np.arange(N):
        sampled = [distribution() for s in range(n)]
        sampled_means.append(np.mean(sampled))
    return sampled_means


def n_scaling(distribution=uniform, *xlimits):
    """Generate a plot to show the std of the mean's 1/sqrt(n) dependence for 3.2 part 2

    For the report, I'll use the "uniform" distribution
    To generate the plot I use in the report run:
    >>> n_scaling(blackjack, 10, 19)
    """
    if not xlimits:
        xlimits = []

    figure()
    subplot(224)
    means = collect_samples(distribution, n=100, N=200)
    print mean(means)
    hist(means, normed=True, bins=20, alpha=0.4)
    title(r"$n=100$")
    xlim(*xlimits)
    # std bar
    errorbar([mean(xlim())], [mean(ylim())/1.5], xerr=std(means), fmt="ro", capsize=5,
        capthick=2, elinewidth=2)
    text(16.1, ylim()[1]*.75, r"$\sigma_{100}=%.2f$" % std(means))

    subplot(223)
    means = collect_samples(distribution, n=50, N=200)
    hist(means, normed=True, bins=20, alpha=0.4)
    title(r"$n=50$")
    xlim(*xlimits)
    errorbar([mean(xlim())], [mean(ylim())/1.5], xerr=std(means), fmt="ro", capsize=5,
        capthick=2, elinewidth=2)
    text(16.1, ylim()[1]*.75, r"$\sigma_{50}=%.2f$" % std(means))

    subplot(222)
    means = collect_samples(distribution, n=10, N=200)
    hist(means, normed=True, bins=30, alpha=0.4)
    title(r"$n=10$")
    xlim(*xlimits)
    errorbar([mean(xlim())], [mean(ylim())/1.5], xerr=std(means), fmt="ro", capsize=5,
        capthick=2, elinewidth=2)
    text(16.1, ylim()[1]*.75, r"$\sigma_{10}=%.2f$" % std(means))

    subplot(221)
    means = collect_samples(distribution, n=5, N=200)
    hist(means, normed=True, bins=30, alpha=0.4)
    title(r"$n=5$")
    xlim(*xlimits)
    errorbar([mean(xlim())], [mean(ylim())/1.5], xerr=std(means), fmt="ro", capsize=5,
        capthick=2, elinewidth=2)
    text(16.1, ylim()[1]*.75, r"$\sigma_5=%.2f$" % std(means))

    show()


def n_scaling_2(distribution):
    """Generate another plot to show the std of the mean's 1/sqrt(n) dependence for 3.2 part 2

    For the report, I'll use the "uniform" distribution
    To generate the plot I use in the report run:
    >>> n_scaling_2(blackjack)
    """
    # look at n values from 1 to 10000
    n_array = np.logspace(0, 4, 100)
    # standard deviations of samples of size 20
    std_array = [np.std(collect_samples(distribution, n=int(n), N=20)) for n in n_array]

    def sig_fit(n, A, B):
        return A * n**(B)
    A, C = curve_fit(sig_fit, n_array, std_array)
    A, B = A
    print C
    fitfunc = lambda n: sig_fit(n, A, B)

    loglog(n_array, std_array, "r.", label=r"sampled")
    loglog(n_array, fitfunc(n_array), "g-", linewidth=2, label=r"fit: $\sigma = %.2fn^{%.2f}$" % (A, B))
    xlabel(r"n (samples)", fontsize=18)
    ylabel(r"$\sigma$ (standard deviation)", fontsize=18)
    xticks(fontsize=14)
    yticks(fontsize=14)
    legend(fontsize=20)
    gca().yaxis.set_major_formatter(ScalarFormatter())
    gca().xaxis.set_major_formatter(ScalarFormatter())
    ticklabel_format(axis='x', style='sci', scilimits=(2,5))
    show()


def approach_gaussian(distribution=uniform):
    """Generate plot for first part of 3.2, showing that larger N appraoches a gaussian

    For the report, I'll use the "blackjack" distribution
    To generate the plot I use in the report run:
    >>> approach_gaussian(blackjack)
    """
    figure()
    subplot(221)
    means50 = collect_samples(distribution, n=100, N=50)
    datas1, bins, _ = hist(means50, normed=True, bins=30, alpha=0.4)
    mu, sigma = norm.fit(means50)
    centers = (bins[:-1] + bins[1:]) / 2
    plot(centers, normpdf(centers, mu, sigma), "r--", linewidth=3)
    title(r"$N=50$")

    subplot(222)
    means500 = collect_samples(distribution, n=100, N=100)
    datas2, bins, _ = hist(means500, normed=True, bins=30, alpha=0.4)
    mu, sigma = norm.fit(means500)
    centers = (bins[:-1] + bins[1:]) / 2
    plot(centers, normpdf(centers, mu, sigma), "r--", linewidth=3)
    title(r"$N=100$")

    subplot(223)
    means10000 = collect_samples(distribution, n=100, N=1000)
    datas3, bins, _ = hist(means10000, normed=True, bins=30, alpha=0.4)
    mu, sigma = norm.fit(means10000)
    centers = (bins[:-1] + bins[1:]) / 2
    plot(centers, normpdf(centers, mu, sigma), "r--", linewidth=3)
    title(r"$N=1000$")

    subplot(224)
    means50000 = collect_samples(distribution, n=100, N=20000)
    datas4, bins, _ = hist(means50000, normed=True, bins=30, alpha=0.4)
    mu, sigma = norm.fit(means50000)
    centers = (bins[:-1] + bins[1:]) / 2
    plot(centers, normpdf(centers, mu, sigma), "r--", linewidth=3)
    title(r"$N=20000$")
    show()


if __name__ == "__main__":
    n_scaling(blackjack, 10, 19)
    n_scaling_2(blackjack)
