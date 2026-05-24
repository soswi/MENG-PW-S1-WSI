# Author: [Student Name] - Warsaw University of Technology
# Course: Introduction to Artificial Intelligence (WSI)
# Assignment 05: Two-layer perceptron - function representation

import numpy as np


class MLP:
    """
    Two-layer perceptron (Multi-Layer Perceptron) with one hidden layer.

    Architecture:
        input layer  (1 neuron)
        hidden layer (n_hidden neurons, sigmoid activation)
        output layer (1 neuron, linear activation)

    Training is performed using gradient descent with backpropagation.
    """

    def __init__(self, n_hidden: int, learning_rate: float, random_seed: int = None):
        """
        Initialize MLP with random weights.

        Parameters
        ----------
        n_hidden : int
            Number of neurons in the hidden layer.
        learning_rate : float
            Step size for gradient descent.
        random_seed : int, optional
            Seed for reproducibility of a single run.
        """
        if random_seed is not None:
            np.random.seed(random_seed)

        # Weights and biases: input -> hidden
        self.W1 = np.random.randn(n_hidden, 1) * 1.0
        self.b1 = np.zeros((n_hidden, 1))

        # Weights and biases: hidden -> output
        self.W2 = np.random.randn(1, n_hidden) * 1.0
        self.b2 = np.zeros((1, 1))

        self.learning_rate = learning_rate
        self.n_hidden = n_hidden

    # ------------------------------------------------------------------
    # Activation function
    # ------------------------------------------------------------------

    def _sigmoid(self, z: np.ndarray) -> np.ndarray:
        """Sigmoid activation function."""
        return 1.0 / (1.0 + np.exp(-z))

    def _sigmoid_derivative(self, sigmoid_output: np.ndarray) -> np.ndarray:
        """Derivative of sigmoid given its output value (s * (1 - s))."""
        return sigmoid_output * (1.0 - sigmoid_output)

    # ------------------------------------------------------------------
    # Forward pass
    # ------------------------------------------------------------------

    def _forward(self, X: np.ndarray):
        """
        Perform forward pass through the network.

        Parameters
        ----------
        X : np.ndarray, shape (1, n_samples)
            Input data.

        Returns
        -------
        output : np.ndarray, shape (1, n_samples)
            Network predictions.
        cache : dict
            Intermediate values needed for backpropagation.
        """
        Z1 = self.W1 @ X + self.b1          # (n_hidden, n_samples)
        A1 = self._sigmoid(Z1)               # (n_hidden, n_samples)

        Z2 = self.W2 @ A1 + self.b2          # (1, n_samples)
        output = Z2                           # linear activation at output

        cache = {"X": X, "Z1": Z1, "A1": A1, "Z2": Z2}
        return output, cache

    # ------------------------------------------------------------------
    # Backward pass
    # ------------------------------------------------------------------

    def _backward(self, output: np.ndarray, y: np.ndarray, cache: dict):
        """
        Compute gradients using backpropagation and update weights.

        Parameters
        ----------
        output : np.ndarray, shape (1, n_samples)
            Network predictions from forward pass.
        y : np.ndarray, shape (1, n_samples)
            Ground truth values.
        cache : dict
            Intermediate values from forward pass.
        """
        # number of samples - used to average the gradient across all training points
        n_samples = y.shape[1]

        # Output layer gradient (MSE derivative: 2*(pred - true) / n, factor 2 absorbed into lr)
        # difference between prediction and ground truth, averaged over all samples
        dZ2 = (output - y) / n_samples       # (1, n_samples)

        # gradient of output weights - how much each W2 weight contributed to the error
        dW2 = dZ2 @ cache["A1"].T            # (1, n_hidden)

        # gradient of output bias - summed over all samples since bias is shared
        db2 = np.sum(dZ2, axis=1, keepdims=True)  # (1, 1)

        # propagate error back through W2 to the hidden layer
        dA1 = self.W2.T @ dZ2               # (n_hidden, n_samples)

        # pass gradient through sigmoid derivative to undo the activation function
        dZ1 = dA1 * self._sigmoid_derivative(cache["A1"])  # (n_hidden, n_samples)

        # gradient of hidden weights - how much each W1 weight contributed to the error
        dW1 = dZ1 @ cache["X"].T            # (n_hidden, 1)

        # gradient of hidden biases - summed over all samples since bias is shared
        db1 = np.sum(dZ1, axis=1, keepdims=True)  # (n_hidden, 1)

        # Gradient descent update
        # subtract gradient scaled by learning rate - move in direction of decreasing error
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------

    def train(self, X: np.ndarray, y: np.ndarray, n_iterations: int):
        """
        Train the network using gradient descent.

        Parameters
        ----------
        X : np.ndarray, shape (n_samples,) or (1, n_samples)
            Input values.
        y : np.ndarray, shape (n_samples,) or (1, n_samples)
            Target values.
        n_iterations : int
            Number of gradient descent steps.
        """
        X = np.atleast_2d(X).reshape(1, -1)
        y = np.atleast_2d(y).reshape(1, -1)

        for _ in range(n_iterations):
            output, cache = self._forward(X)
            self._backward(output, y, cache)

    # ------------------------------------------------------------------
    # Prediction
    # ------------------------------------------------------------------

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict output values for given inputs.

        Parameters
        ----------
        X : np.ndarray, shape (n_samples,) or (1, n_samples)
            Input values.

        Returns
        -------
        np.ndarray, shape (n_samples,)
            Predicted values.
        """
        X = np.atleast_2d(X).reshape(1, -1)
        output, _ = self._forward(X)
        return output.flatten()


# ------------------------------------------------------------------
# Metrics
# ------------------------------------------------------------------

def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Squared Error between true and predicted values."""
    return float(np.mean((y_true - y_pred) ** 2))


def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error between true and predicted values."""
    return float(np.mean(np.abs(y_true - y_pred)))
