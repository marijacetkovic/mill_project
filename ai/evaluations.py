
INF = 1000
MAX_DEPTH = 5


def evaluate_state(state, player):
    opponent = 3 - player
    score = 0

    # mill formation
    score += count_mills(state, player) * 300
    score -= count_mills(state, opponent) * 300  # prevent opponent mills

    # potential mill formation
    score += count_potential_mills(state, player) * 100
    score -= count_potential_mills(state, opponent) * 100  

    #piece count
    score += (state.count_pieces(player) - state.count_pieces(opponent)) * 100

    #move advantage
    score += len(state.legal_moves(player)) * 5
    score -= len(state.legal_moves(opponent)) * 5

    return score

def count_mills(state, player):
    count = 0
    for pos in range(1, 25):
        if state._board[pos] == player and state._in_mill(pos):
            count += 1
    return count // 3


def count_potential_mills(state, player):
    potential_mills = 0

    for mill in state.mills:
        player_count = 0
        empty_count = 0

        for pos in mill:
            if state._board[pos] == player:
                player_count += 1
            elif state._board[pos] == 0: 
                empty_count += 1

        if player_count == 2 and empty_count == 1:
            potential_mills += 1

    return potential_mills
