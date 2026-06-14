# Author: Wiktor Sosnowski, 348561

import numpy as np


def sphere(x: np.ndarray) -> float:
    """
    Sphere function: f(x) = x1^2 + x2^2
    Global minimum: f(0, 0) = 0
    Domain: x_i in [-10, 10]
    """
    return float(np.sum(x ** 2))


def matyas(x: np.ndarray) -> float:
    """
    Matyas function (2D): f(x) = 0.26*(x1^2 + x2^2) - 0.48*x1*x2
    Global minimum: f(0, 0) = 0
    Domain: x_i in [-10, 10]
    """
    return 0.26 * (x[0] ** 2 + x[1] ** 2) - 0.48 * x[0] * x[1]
