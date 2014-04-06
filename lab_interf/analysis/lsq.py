import numpy as np


def fit_components(x, y, *component_funcs):
    M, N = len(x), len(component_funcs)

    X = np.ones((M, N))
    for i, func in enumerate(component_funcs):
        X[:, i] = func(x)

    Y = y
    XX = np.dot(np.transpose(X), X)
    XY = np.dot(np.transpose(X), Y)
    XXI = np.linalg.inv(XX)
    a = np.dot(XXI, XY)
    Y_ = np.dot(X, a)

    delta_Y = Y - Y_
    s2 = np.sum(delta_Y**2) / (M-N)

    cov = s2 * XXI

    return a, Y_, s2, cov
