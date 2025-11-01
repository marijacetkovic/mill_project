from famnit_gym.envs import mill
from ai.minimax import minimax
from ai.evaluations import INF
from ai.utility import get_state_hash


def get_optimal_move(current_state, current_player):
    best_score, best_move, opponent = -INF, None, 3 - current_player
    legal_moves = current_state.legal_moves(player=current_player)
    visited = {get_state_hash(current_state)}
    if not legal_moves:   
        return None
    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(current_player, move)
        score = minimax(next_state, opponent, False, 1, visited.copy())

        if score > best_score:
            best_score, best_move = score, move

    return best_move


