INF = 1000


def evaluate_state(current_state, maximizing_player):
    if maximizing_player == 1:
        p1_pieces = current_state.count_pieces(1)
        p2_pieces = current_state.count_pieces(2)
        piece_advantage = (p1_pieces - p2_pieces) * 8
        position_score = evaluate_positions(current_state, 1, 2)
    else:
        p1_pieces = current_state.count_pieces(1)
        p2_pieces = current_state.count_pieces(2)
        piece_advantage = (p2_pieces - p1_pieces) * 8
        position_score = evaluate_positions(current_state, 2, 1)

    score = piece_advantage + position_score

    return score

def evaluate_positions(current_state, player, opponent):
    score = 0
    board_state = current_state.get_state()

    position_values = {
        4: 4, 5: 4, 6: 4, 14: 4, 21: 4, 20: 4, 19: 4, 11: 4,
        1: 3, 2: 3, 3: 3, 15: 3, 24: 3, 23: 3, 22: 3, 10: 3,
        7: 3, 8: 3, 9: 3, 13: 3, 18: 3, 17: 3, 16: 3, 12: 3
    }

    for pos, value in position_values.items():
        if board_state[pos - 1] == player:
            score += value
        elif board_state[pos - 1] == opponent:
            score -= value

    return score
