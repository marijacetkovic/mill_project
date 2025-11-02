from evaluations import INF
from minimax import minimax, get_state_hash
import random

class AIPlayer:
    def __init__(self, player_id, difficulty="medium"):
        self.player_id = player_id
        self.difficulty = difficulty
        self.depth_settings = {
            "easy": 2,
            "medium": 4,
            "hard": 5  
        }
        self.rnd_settings = {
            "easy": 0.3,
            "medium": 0,
            "hard": 0  
        }

    def choose_move(self, state):
        max_depth = self.depth_settings.get(self.difficulty)

        legal_moves = state.legal_moves(self.player_id)
        if not legal_moves:
            return None

        if random.random() < self.rnd_settings.get(self.difficulty):
            return random.choice(legal_moves)

        best_score = -INF
        best_move = None
        opponent = 3 - self.player_id
        visited = {get_state_hash(state)}

        for move in legal_moves:
            next_state = state.clone()
            next_state.make_move(self.player_id, move)
            score = minimax(next_state, opponent, False, 1, visited.copy(), max_depth)
            if score > best_score:
                best_score, best_move = score, move

        return best_move

