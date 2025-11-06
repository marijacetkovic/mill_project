from .evaluations import INF, evaluate_state
from .utility import get_state_hash


def minimax(current_state, current_player, maximizing_player, maximizing, depth, max_depth, visited_states=None,
            alpha=-INF, beta=INF):
    if visited_states is None:
        visited_states = set()

    state_hash = get_state_hash(current_state)
    if state_hash in visited_states:
        return 0
    visited_states.add(state_hash)

    # Check for terminal state
    # if current_state.game_over():
    #     terminal_reward = INF - depth
    #     return -terminal_reward if maximizing else terminal_reward
    
    if current_state.game_over():
        if current_state._player[maximizing_player]['phase'] == 'lost':
            return -INF + depth
        elif current_state._player[3 - maximizing_player]['phase'] == 'lost':
            return INF - depth   
        else:
            return 0  

    # Depth limit reached
    if depth >= max_depth:
        return evaluate_state(current_state, maximizing_player)
    

    opponent = 3 - current_player
    best_score = -INF if maximizing else INF
    legal_moves = current_state.legal_moves(current_player)

    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(current_player, move)

        score = minimax(
            next_state,
            opponent,
            maximizing_player,
            not maximizing,
            depth + 1,
            max_depth,
            visited_states.copy(),
            alpha,
            beta
        )

        if maximizing:
            if score > best_score:
                best_score = score
            if score > alpha:
                alpha = score
        else:
            if score < best_score:
                best_score = score
            if score < beta:
                beta = score

        if beta <= alpha:
            break

    return best_score
