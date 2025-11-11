from minimax_implementations import limited_depth
import random


# CLASS THAT REPRESENTS DIFFERENT DIFFICULTIES
class AiPlayerWithDifficulty:
    def __init__(self, player_id, difficulty):
        self.player_id = player_id
        self.difficulty = difficulty

        # THE CONTROL PARAMETERS ARE MAXIMUM DEPTH AND RATIO OF RANDOM MOVES
        self.MAX_DEPTH_SETTINGS = {
            "apprentice": 1,
            "adventurer": 2,
            "knight": 3,
            "champion": 5,
            "legend": 6
        }

        self.NUM_RANDOM_MOVES_SETTINGS = {
            "apprentice": 1,
            "adventurer": 0.4,
            "knight": 0.3,
            "champion": 0.1,
            "legend": 0.0,
        }

    # GETTERS
    def get_max_depth(self):
        return self.MAX_DEPTH_SETTINGS[self.difficulty]

    def get_num_random_moves(self):
        return self.NUM_RANDOM_MOVES_SETTINGS[self.difficulty]

    # COMPUTE MOVE METHOD
    def choose_move(self, current_state, num_moves_already_done):
        max_depth = self.get_max_depth()
        num_random_moves = self.get_num_random_moves()

        legal_moves = current_state.legal_moves(self.player_id)

        # RANDOM MOVE
        if random.random() < num_random_moves:
            return random.choice(legal_moves)

        # OPTIMAL MOVE
        return limited_depth.find_optimal_move(current_state=current_state,
                                               maximizing_player=self.player_id,
                                               max_depth=max_depth,
                                               moves_counter=num_moves_already_done)
