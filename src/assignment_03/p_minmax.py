"""
Author: Katarzyna Nałęcz-Charkiewicz (original structure)
Modified by: Wiktor Sosnowski (implementation of make_move, minimax, evaluate)
"""

import math

from board import Board
from player import Player


class MinMaxPlayer(Player):
    def __init__(self, name: str, depth_limit: int):
        super().__init__(name)
        self.depth_limit = depth_limit

    def make_move(self, board: Board, your_side: str):
        """Choose the best move using minimax with alpha-beta pruning."""
        _, best_move = self.minimax(
            board, your_side, depth=0,
            alpha=-math.inf, beta=math.inf,
            maximizing=True
        )
        return best_move

    def minimax(
        self, board: Board, side: str, depth: int,
        alpha: float = -math.inf, beta: float = math.inf,
        maximizing: bool = True
    ):
        """
        Minimax with alpha-beta pruning.

        'side' is the perspective of the MAX player (the one who called make_move).
        Returns (score, best_move_index).
        """
        winner = board.who_is_winner()

        # Terminal: someone won
        if winner is not None:
            return (1, None) if winner == side else (-1, None)

        empty = board.empty_indexes()

        # Terminal: draw
        if not empty:
            return 0, None

        # Depth limit reached — use heuristic
        if depth >= self.depth_limit:
            return self.evaluate(board, side), None

        best_move = None

        if maximizing:
            best_score = -math.inf
            for idx in empty:
                child = board.clone()
                child.register_move(idx)
                score, _ = self.minimax(
                    child, side, depth + 1, alpha, beta, maximizing=False
                )
                if score > best_score:
                    best_score = score
                    best_move = idx
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # beta cut-off
            return best_score, best_move
        else:
            best_score = math.inf
            for idx in empty:
                child = board.clone()
                child.register_move(idx)
                score, _ = self.minimax(
                    child, side, depth + 1, alpha, beta, maximizing=True
                )
                if score < best_score:
                    best_score = score
                    best_move = idx
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # alpha cut-off
            return best_score, best_move

    def evaluate(self, board: Board, side: str) -> float:
        """
        Heuristic for non-terminal states at depth limit.

        Counts lines (rows, columns, diagonals) open for 'side' minus lines
        open for the opponent. A line is open if it contains no opponent pieces.
        Result is normalised to (-1, 1).
        """
        opponent = (
            board.char_cross if side == board.char_circle else board.char_circle
        )

        lines = []
        lines.append(((0, 0), (1, 1)))                   # main diagonal
        lines.append(((board.size - 1, 0), (-1, 1)))     # anti-diagonal
        for i in range(board.size):
            lines.append(((i, 0), (0, 1)))               # row i
            lines.append(((0, i), (1, 0)))               # column i

        my_open = 0
        opp_open = 0

        for (start, step) in lines:
            has_mine = False
            has_opp = False
            point = start
            while 0 <= point[0] < board.size and 0 <= point[1] < board.size:
                cell = board.board[point[0] * board.size + point[1]]
                if cell == side:
                    has_mine = True
                elif cell == opponent:
                    has_opp = True
                point = (point[0] + step[0], point[1] + step[1])
            if has_mine and not has_opp:
                my_open += 1
            if has_opp and not has_mine:
                opp_open += 1

        total_lines = 2 + 2 * board.size  # 2 diagonals + rows + columns
        return (my_open - opp_open) / total_lines
