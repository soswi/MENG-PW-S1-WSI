# Author: Wiktor Sosnowski, 348561

import numpy as np
from numerical_gradient import numerical_gradient


class GradientDescent:
    """
    Gradient descent optimizer for arbitrary differentiable functions.

    Stop conditions:
        - gradient norm falls below grad_tol (convergence)
        - number of iterations reaches max_iter (safety limit)
    """

    def __init__(
        self,
        learning_rate: float = 0.1,
        max_iter: int = 10000,
        grad_tol: float = 1e-6,
    ):
        """
        Args:
            learning_rate: step size for each gradient update
            max_iter:      maximum number of iterations
            grad_tol:      gradient norm threshold for convergence
        """
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.grad_tol = grad_tol

    def optimize(self, func: callable, x0: np.ndarray) -> dict:
        """
        Run gradient descent starting from x0.

        Args:
            func: objective function to minimize, takes np.ndarray, returns scalar
            x0:   starting point

        Returns:
            result dict with keys:
                x_opt       - best point found
                f_opt       - function value at x_opt
                n_iter      - number of iterations performed
                trajectory  - array of shape (n_iter+1, 2) with all visited points
                f_history   - list of function values at each iteration
                converged   - True if stopped due to gradient norm, False if max_iter reached
        """
        x = x0.copy().astype(float)
        trajectory = [x.copy()]
        f_history = [func(x)]

        for i in range(self.max_iter):
            grad = numerical_gradient(func, x)

            # check convergence: stop if gradient is flat enough
            if np.linalg.norm(grad) < self.grad_tol:
                return self._build_result(x, func, i, trajectory, f_history, converged=True)

            # gradient descent update step
            x = x - self.learning_rate * grad
            trajectory.append(x.copy())
            f_history.append(func(x))

        return self._build_result(x, func, self.max_iter, trajectory, f_history, converged=False)

    def _build_result(
        self,
        x: np.ndarray,
        func: callable,
        n_iter: int,
        trajectory: list,
        f_history: list,
        converged: bool,
    ) -> dict:
        return {
            "x_opt": x,
            "f_opt": func(x),
            "n_iter": n_iter,
            "trajectory": np.array(trajectory),
            "f_history": f_history,
            "converged": converged,
        }
