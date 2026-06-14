# Author: Wiktor Sosnowski, 348561

import numpy as np
import matplotlib.pyplot as plt


DOMAIN_MIN = -10
DOMAIN_MAX = 10
PLOT_RESOLUTION = 200


def plot_convergence(
    f_histories: list,
    labels: list,
    title: str,
    ax: plt.Axes = None,
) -> plt.Axes:
    """
    Plot objective function value vs iteration number for multiple runs.

    Args:
        f_histories: list of f_history lists (one per run)
        labels:      list of label strings (one per run)
        title:       plot title
        ax:          optional existing Axes to draw on

    Returns:
        ax: the Axes object with the plot
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    for f_history, label in zip(f_histories, labels):
        ax.plot(f_history, label=label)

    ax.set_xlabel("Iteration")
    ax.set_ylabel("Objective function value")
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    return ax


def plot_convergence_log(
    f_histories: list,
    labels: list,
    title: str,
    ax: plt.Axes = None,
) -> plt.Axes:
    """
    Same as plot_convergence but with logarithmic y-axis.
    Useful when values span many orders of magnitude.
    """
    ax = plot_convergence(f_histories, labels, title, ax)
    ax.set_yscale("log")
    ax.set_ylabel("Objective function value (log scale)")
    return ax


def plot_trajectory(
    func: callable,
    trajectory: np.ndarray,
    title: str,
    ax: plt.Axes = None,
) -> plt.Axes:
    """
    Plot trajectory of gradient descent on a color mesh of the objective function.
    Based on visualize_fun provided in the assignment.

    Args:
        func:       objective function f(x: np.ndarray) -> float
        trajectory: array of shape (n_steps, 2) with visited points
        title:      plot title
        ax:         optional existing Axes to draw on

    Returns:
        ax: the Axes object with the plot
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 6))

    # build grid for color mesh
    x1 = np.linspace(DOMAIN_MIN, DOMAIN_MAX, PLOT_RESOLUTION)
    x2 = np.linspace(DOMAIN_MIN, DOMAIN_MAX, PLOT_RESOLUTION)
    X1, X2 = np.meshgrid(x1, x2)

    # evaluate func on grid -- func expects np.ndarray, so we vectorize
    Z = np.vectorize(lambda a, b: func(np.array([a, b])))(X1, X2)

    mesh = ax.pcolormesh(X1, X2, Z, cmap="viridis", shading="auto")
    plt.colorbar(mesh, ax=ax, label="Objective function value")

    # draw trajectory
    ax.plot(
        trajectory[:, 0],
        trajectory[:, 1],
        marker="o",
        color="red",
        label="Gradient descent steps",
        alpha=0.6,
        markersize=3,
    )

    # mark start and end
    ax.scatter(
        trajectory[0, 0], trajectory[0, 1],
        color="white", zorder=5, s=60, label="Start"
    )
    ax.scatter(
        trajectory[-1, 0], trajectory[-1, 1],
        color="yellow", zorder=5, s=60, label="Minimum found"
    )

    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_title(title)
    ax.legend(fontsize=8)
    return ax
