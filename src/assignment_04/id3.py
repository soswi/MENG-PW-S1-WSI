# Author: Wiktor Sosnowski, 348561
# ID3 decision tree classifier with maximum depth constraint.

import numpy as np
from collections import Counter


def entropy(labels):
    """Calculate Shannon entropy of a label array."""
    n = len(labels)
    if n == 0:
        return 0.0
    counts = Counter(labels)
    result = 0.0
    for count in counts.values():
        p = count / n
        if p > 0:
            result -= p * np.log2(p)
    return result


def information_gain(labels, subsets):
    """
    Calculate information gain of a split.
    subsets: list of label arrays, one per branch of the split.
    """
    n = len(labels)
    weighted_entropy = sum(
        (len(subset) / n) * entropy(subset)
        for subset in subsets
    )
    return entropy(labels) - weighted_entropy


class Node:
    """A single node in the decision tree."""

    def __init__(self):
        self.feature_index = None    # index of feature to split on (internal node)
        self.children = {}           # maps feature value -> child Node
        self.label = None            # predicted class label (leaf node)

    def is_leaf(self):
        return self.label is not None


class DecisionTreeID3:
    """
    Decision tree classifier using the ID3 algorithm.
    Supports categorical features and optional maximum depth constraint.

    Parameters
    ----------
    max_depth : int or None
        Maximum depth of the tree. None means no limit.
    """

    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.root = None

    def fit(self, X, y):
        """
        Build the decision tree from training data.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
            Feature matrix (categorical values as strings or ints).
        y : np.ndarray of shape (n_samples,)
            Target labels.
        """
        feature_indices = list(range(X.shape[1]))
        self.root = self._build(X, y, feature_indices, depth=0)

    def _build(self, X, y, available_features, depth):
        """Recursively build the tree."""
        node = Node()

        # All samples have the same label — make a leaf
        if len(set(y)) == 1:
            node.label = y[0]
            return node

        # No features left or depth limit reached — majority vote leaf
        if not available_features or (self.max_depth is not None and depth >= self.max_depth):
            node.label = Counter(y).most_common(1)[0][0]
            return node

        # Choose the best feature by information gain
        best_feature = self._best_feature(X, y, available_features)
        node.feature_index = best_feature

        remaining_features = [f for f in available_features if f != best_feature]

        # Split on each unique value of the chosen feature
        for value in np.unique(X[:, best_feature]):
            mask = X[:, best_feature] == value
            X_sub, y_sub = X[mask], y[mask]

            if len(y_sub) == 0:
                # Empty branch — assign majority label from current node
                child = Node()
                child.label = Counter(y).most_common(1)[0][0]
            else:
                child = self._build(X_sub, y_sub, remaining_features, depth + 1)

            node.children[value] = child

        return node

    def _best_feature(self, X, y, available_features):
        """Return the feature index with the highest information gain."""
        best_gain = -1
        best_feature = available_features[0]

        for feature in available_features:
            values = np.unique(X[:, feature])
            subsets = [y[X[:, feature] == v] for v in values]
            gain = information_gain(y, subsets)
            if gain > best_gain:
                best_gain = gain
                best_feature = feature

        return best_feature

    def predict(self, X):
        """
        Predict class labels for samples in X.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        np.ndarray of shape (n_samples,)
        """
        return np.array([self._predict_single(x, self.root) for x in X])

    def _predict_single(self, x, node):
        """Traverse the tree for a single sample."""
        if node.is_leaf():
            return node.label

        value = x[node.feature_index]

        if value in node.children:
            return self._predict_single(x, node.children[value])
        else:
            # Unseen value at prediction time — return most common child label
            labels = self._collect_labels(node)
            return Counter(labels).most_common(1)[0][0]

    def _collect_labels(self, node):
        """Collect all leaf labels in the subtree rooted at node."""
        if node.is_leaf():
            return [node.label]
        labels = []
        for child in node.children.values():
            labels.extend(self._collect_labels(child))
        return labels


def accuracy(y_true, y_pred):
    """Calculate classification accuracy."""
    return np.mean(y_true == y_pred)


def confusion_matrix(y_true, y_pred, classes=None):
    """
    Compute confusion matrix.

    Parameters
    ----------
    y_true, y_pred : array-like
    classes : list, optional. If None, inferred from data.

    Returns
    -------
    matrix : np.ndarray of shape (n_classes, n_classes)
    classes : list of class labels (row/column order)
    """
    if classes is None:
        classes = sorted(set(y_true) | set(y_pred))
    class_index = {c: i for i, c in enumerate(classes)}
    n = len(classes)
    matrix = np.zeros((n, n), dtype=int)
    for true, pred in zip(y_true, y_pred):
        matrix[class_index[true]][class_index[pred]] += 1
    return matrix, classes
