# Author: Wiktor Sosnowski, 348561

import numpy as np


def numerical_gradient(func: callable, x: np.ndarray, h: float = 1e-5) -> np.ndarray:
    """
    Compute gradient of func at point x using central finite differences.

    Args:
        func: objective function, takes np.ndarray, returns scalar
        x:    point at which gradient is evaluated
        h:    step size for finite difference approximation

    Returns:
        grad: gradient vector of the same shape as x
    """
    grad = np.zeros_like(x, dtype=float)
    for i in range(len(x)):
        # perturb x[i] forward and backward
        x_forward = x.copy()
        x_backward = x.copy()
        x_forward[i] += h
        x_backward[i] -= h
        # central difference formula: (f(x+h) - f(x-h)) / (2h)
        grad[i] = (func(x_forward) - func(x_backward)) / (2 * h)
    return grad
