# Author: Wiktor Sosnowski, 348561

import numpy as np


def load_tsplib(filepath: str) -> tuple[np.ndarray, list[str]]:
    """
    Parse a TSPLIB .tsp file (EUC_2D edge weight type).
    Returns (coords, city_names) where coords is shape (n, 2).
    """
    coords = []
    city_names = []
    in_node_section = False

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                in_node_section = True
                continue
            if line in ("EOF", ""):
                if in_node_section:
                    break
                continue
            if in_node_section:
                parts = line.split()
                city_names.append(parts[0])
                coords.append([float(parts[1]), float(parts[2])])

    return np.array(coords), city_names


def build_distance_matrix(coords: np.ndarray) -> np.ndarray:
    """
    Compute Euclidean distance matrix (rounded to nearest int, TSPLIB standard).
    Returns symmetric matrix of shape (n, n).
    """
    n = len(coords)
    dist = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = coords[i, 0] - coords[j, 0]
                dy = coords[i, 1] - coords[j, 1]
                dist[i, j] = round(np.sqrt(dx * dx + dy * dy))
    return dist


def tour_length(tour: np.ndarray, dist_matrix: np.ndarray) -> float:
    """
    Compute total length of a tour (closed loop).
    tour: 1D array of city indices, length n.
    """
    n = len(tour)
    total = 0.0
    for i in range(n):
        total += dist_matrix[tour[i], tour[(i + 1) % n]]
    return total


def fitness(tour: np.ndarray, dist_matrix: np.ndarray) -> float:
    """
    Fitness = 1 / tour_length. Higher is better.
    """
    return 1.0 / tour_length(tour, dist_matrix)
