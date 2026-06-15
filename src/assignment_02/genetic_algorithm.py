# Author: Wiktor Sosnowski, 348561

import numpy as np
from tsp_utils import tour_length, fitness


class GeneticAlgorithm:
    """
    Genetic algorithm for the symmetric TSP.

    Supports:
      - Roulette wheel selection
      - Tournament selection
      - One-point crossover with order repair
      - Swap mutation
      - Generational succession (full population replacement)
    """

    def __init__(
        self,
        dist_matrix: np.ndarray,
        pop_size: int = 100,
        mutation_prob: float = 0.01,
        n_generations: int = 500,
        selection: str = "roulette",   # "roulette" or "tournament"
        tournament_size: int = 3,
        seed: int | None = None,
    ):
        self.dist_matrix = dist_matrix
        self.n_cities = dist_matrix.shape[0]
        self.pop_size = pop_size
        self.mutation_prob = mutation_prob
        self.n_generations = n_generations
        self.selection = selection
        self.tournament_size = tournament_size
        self.rng = np.random.default_rng(seed)

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def _init_population(self) -> np.ndarray:
        """Create pop_size random permutations of city indices."""
        pop = np.array([
            self.rng.permutation(self.n_cities)
            for _ in range(self.pop_size)
        ])
        return pop

    # ------------------------------------------------------------------
    # Fitness
    # ------------------------------------------------------------------

    def _evaluate(self, population: np.ndarray) -> np.ndarray:
        """Return fitness array for entire population."""
        return np.array([
            fitness(ind, self.dist_matrix) for ind in population
        ])

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

    def _roulette_select(self, population: np.ndarray, fitnesses: np.ndarray) -> np.ndarray:
        """
        Roulette wheel (fitness-proportionate) selection.
        Returns one individual.
        """
        total = fitnesses.sum()
        probs = fitnesses / total
        idx = self.rng.choice(len(population), p=probs)
        return population[idx].copy()

    def _tournament_select(self, population: np.ndarray, fitnesses: np.ndarray) -> np.ndarray:
        """
        Tournament selection.
        Randomly picks tournament_size individuals; returns the best.
        """
        contenders = self.rng.choice(len(population), size=self.tournament_size, replace=False)
        best = contenders[np.argmax(fitnesses[contenders])]
        return population[best].copy()

    def _select(self, population: np.ndarray, fitnesses: np.ndarray) -> np.ndarray:
        """Dispatch to the configured selection method."""
        if self.selection == "roulette":
            return self._roulette_select(population, fitnesses)
        elif self.selection == "tournament":
            return self._tournament_select(population, fitnesses)
        else:
            raise ValueError(f"Unknown selection method: {self.selection}")

    # ------------------------------------------------------------------
    # Crossover
    # ------------------------------------------------------------------

    def _one_point_crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        """
        One-point crossover adapted for permutation representation.

        Steps:
          1. Copy parent1[0:point] into child.
          2. Fill remaining positions with cities from parent2
             in order, skipping cities already in child.

        This preserves the permutation property (no duplicates).
        """
        n = self.n_cities
        point = self.rng.integers(1, n)  # crossover point in [1, n-1]

        child = np.full(n, -1, dtype=int)
        child[:point] = parent1[:point]

        # cities already placed
        placed = set(child[:point])

        # fill from parent2 in order, skipping already placed cities
        fill_pos = point
        for city in parent2:
            if city not in placed:
                child[fill_pos] = city
                fill_pos += 1

        return child

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def _swap_mutation(self, individual: np.ndarray) -> np.ndarray:
        """
        Swap mutation: with probability mutation_prob, swap two random cities.
        Operates in-place on a copy.
        """
        ind = individual.copy()
        if self.rng.random() < self.mutation_prob:
            i, j = self.rng.choice(self.n_cities, size=2, replace=False)
            ind[i], ind[j] = ind[j], ind[i]
        return ind

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self) -> dict:
        """
        Execute the genetic algorithm.

        Returns a dict with:
          - best_tour: best individual found
          - best_length: its tour length
          - history: list of best tour length per generation
        """
        population = self._init_population()
        fitnesses = self._evaluate(population)

        best_idx = np.argmax(fitnesses)
        best_tour = population[best_idx].copy()
        best_length = tour_length(best_tour, self.dist_matrix)

        history = [best_length]

        for _ in range(self.n_generations):
            new_population = []

            # generational succession: replace entire population
            for _ in range(self.pop_size):
                parent1 = self._select(population, fitnesses)
                parent2 = self._select(population, fitnesses)
                child = self._one_point_crossover(parent1, parent2)
                child = self._swap_mutation(child)
                new_population.append(child)

            population = np.array(new_population)
            fitnesses = self._evaluate(population)

            # track best
            gen_best_idx = np.argmax(fitnesses)
            gen_best_length = tour_length(population[gen_best_idx], self.dist_matrix)
            if gen_best_length < best_length:
                best_length = gen_best_length
                best_tour = population[gen_best_idx].copy()

            history.append(best_length)

        return {
            "best_tour": best_tour,
            "best_length": best_length,
            "history": history,
        }
