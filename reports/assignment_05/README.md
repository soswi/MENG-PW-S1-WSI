# WSI - Assignment 05: Two-layer perceptron

## Project structure

```
.
├── README.md
├── requirements.txt
│
├── src/
│   └── assignment_05/
│       └── mlp.py                  <- MLP class
│
├── notebooks/
│   └── assignment_05/
│       └── assignment_05.ipynb     <- notebook with experiments
│
├── data/
│   └── assignment_05/
│       ├── raw/
│       │   └── laplace_raw.csv     <- raw data (x, f(x))
│       └── processed/
│           └── laplace_processed.csv <- data after normalization/split
│
├── docs/
│   └── assignment_05/
│       └── assignment_05.pdf       <- task description
│
└── reports/
    └── assignment_05/
        └── report_05.pdf           <- report
```

---

## MLP class description (`src/assignment_05/mlp.py`)

The `MLP` class implements a two-layer perceptron with one hidden layer.

### Variables

| Variable | Description |
|----------|-------------|
| `W1` | weight matrix between input and hidden layer, shape (n_hidden, 1) |
| `b1` | hidden layer bias, shape (n_hidden, 1) |
| `W2` | weight matrix between hidden layer and output, shape (1, n_hidden) |
| `b2` | output layer bias, shape (1, 1) |
| `learning_rate` | step size for gradient descent |
| `n_hidden` | number of neurons in the hidden layer |

---

### Methods

#### `__init__(n_hidden, learning_rate, random_seed)`
Initializes the network. Weights `W1` and `W2` are sampled from a normal distribution, biases are set to zero.

- `n_hidden` - number of neurons in the hidden layer
- `learning_rate` - step size for gradient descent
- `random_seed` - optional seed for reproducibility of a single run

---

#### `_sigmoid(z)`
Computes the sigmoid activation function: `1 / (1 + exp(-z))`. Used as the activation function of the hidden layer. Returns values in range (0, 1).

- input: array `z`
- output: array of the same shape

---

#### `_sigmoid_derivative(sigmoid_output)`
Computes the derivative of sigmoid given its output: `s * (1 - s)`. Used during backpropagation.

- input: output of sigmoid (already processed by `_sigmoid`, not raw `z`)
- output: array of derivatives

---

#### `_forward(X)`
Performs a forward pass through the network - computes network output for given inputs.

- input: `X` - input array, shape (1, n_samples)
- output: `output` - predicted values, shape (1, n_samples); `cache` - dictionary with intermediate values needed for backpropagation (X, Z1, A1, Z2)

---

#### `_backward(output, y, cache)`
Performs backpropagation - computes gradients and updates weights using gradient descent.

- `output` - network output from `_forward`
- `y` - ground truth values, shape (1, n_samples)
- `cache` - intermediate values from `_forward`

Returns nothing - directly modifies `W1`, `b1`, `W2`, `b2`.

---

#### `train(X, y, n_iterations)`
Training loop - performs `n_iterations` gradient descent steps. For each step calls `_forward` and `_backward`.

- `X` - input data
- `y` - target values
- `n_iterations` - number of training iterations

---

#### `predict(X)`
Returns predicted values for given inputs. Calls `_forward` only.

- input: `X` - input data
- output: array of predicted values, shape (n_samples,)

---

### Helper functions

#### `mean_squared_error(y_true, y_pred)`
Computes Mean Squared Error (MSE) between true and predicted values.

#### `mean_absolute_error(y_true, y_pred)`
Computes Mean Absolute Error (MAE) between true and predicted values.
