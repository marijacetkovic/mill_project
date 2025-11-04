
from evaluations import INF, MAX_DEPTH, evaluate_state
from utility import get_state_hash


def minimax(current_state, current_player, maximizing, depth, visited_states=None, max_depth = MAX_DEPTH, alpha=-INF, beta=INF):
    if visited_states is None:
        visited_states = set()

    state_hash = get_state_hash(current_state)
    terminal_reward = INF - depth

    if state_hash in visited_states:
        return -terminal_reward if maximizing else terminal_reward
    else:
        visited_states.add(state_hash)


    if current_state.game_over():  # game over
        return 0

    if depth == max_depth:
        return evaluate_state(current_state, current_player)
    

    opponent = 3 - current_player
    best_score = -INF if maximizing else INF
    legal_moves = current_state.legal_moves(current_player)
    if not legal_moves:
        return -terminal_reward if maximizing else terminal_reward
    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(current_player, move)
        score = minimax(next_state, opponent, not maximizing, depth + 1, visited_states.copy(), alpha, beta)

        if maximizing:
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
        else:
            best_score = min(best_score, score)
            beta = min(beta, best_score)

        if alpha >= beta:
            break

    return best_score