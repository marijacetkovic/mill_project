from evaluations import INF
from minimax import minimax
from utility import get_state_hash
import random


class AIPlayer:
    def __init__(self, player_id, difficulty="medium"):
        self.player_id = player_id
        self.difficulty = difficulty
        self.depth_settings = {
            "easy": 2,
            "medium": 3,
            "hard": 4
        }
        self.rnd_settings = {
            "easy": 0.3,
            "medium": 0.1,
            "hard": 0
        }

    def choose_move(self, state):
        max_depth = self.depth_settings.get(self.difficulty, 3)

        legal_moves = state.legal_moves(self.player_id)
        if not legal_moves:
            return None

        # Random move based on difficulty
        if random.random() < self.rnd_settings.get(self.difficulty, 0):
            return random.choice(legal_moves)

        best_score = -INF
        best_move = None
        opponent = 3 - self.player_id

        for move in legal_moves:
            next_state = state.clone()
            next_state.make_move(self.player_id, move)

            score = minimax(
                next_state,
                opponent,
                self.player_id,  # maximizing_player
                False,  # maximizing
                0,  # depth
                max_depth,
                None  # visited_states
            )

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
