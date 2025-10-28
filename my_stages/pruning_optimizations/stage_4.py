from famnit_gym.envs import mill
import hashlib


INF = 1000
MAX_DEPTH = 995


def get_state_hash(current_state):
    state_data = (
        current_state.get_state(),
        current_state.get_phase(1),
        current_state.get_phase(2),
        current_state.count_pieces(1),
        current_state.count_pieces(2),
    )

    return hashlib.md5(str(state_data).encode()).hexdigest()


def evaluate_state(current_state, current_player):
    opponent = 3 - current_player

    # 1. Piece count advantage (most important factor)
    my_pieces = current_state.count_pieces(current_player)
    opp_pieces = current_state.count_pieces(opponent)
    piece_advantage = (my_pieces - opp_pieces) * 100

    # 2. Phase advantage (being in a later phase is better)
    my_phase = current_state.get_phase(current_player)
    opp_phase = current_state.get_phase(opponent)
    phase_advantage = (opp_phase - my_phase) * 50  # Negative if opponent is in later phase

    # 3. Potential mills evaluation
    my_potential_mills = count_potential_mills(current_state, current_player)
    opp_potential_mills = count_potential_mills(current_state, opponent)
    mill_potential = (my_potential_mills - opp_potential_mills) * 30

    # 4. Mobility evaluation (number of legal moves)
    my_mobility = len(current_state.legal_moves(current_player))
    opp_mobility = len(current_state.legal_moves(opponent))
    mobility_advantage = (my_mobility - opp_mobility) * 5

    # 5. Piece positioning (central positions are better)
    position_score = evaluate_positions(current_state, current_player, opponent)

    # 6. Blocking opponent's potential mills
    blocking_score = evaluate_blocking(current_state, current_player, opponent)

    # 7. Game phase specific bonuses
    phase_bonus = evaluate_phase_bonus(current_state, current_player, my_phase, opp_phase)

    # Combine all components
    score = (piece_advantage + phase_advantage + mill_potential +
             mobility_advantage + position_score + blocking_score + phase_bonus)

    return score


def count_potential_mills(current_state, player):
    potential_mills = 0
    board_state = current_state.get_state()

    # Define all possible mill lines (rows, columns, and diagonals where applicable)
    mill_lines = [
        # Horizontal lines
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [9, 10, 11], [12, 13, 14], [15, 16, 17],
        [18, 19, 20], [21, 22, 23],
        # Vertical lines
        [0, 9, 21], [3, 10, 18], [6, 11, 15],
        [1, 4, 7], [16, 19, 22], [8, 12, 17],
        [5, 13, 20], [2, 14, 23]
    ]

    for line in mill_lines:
        player_count = 0
        empty_count = 0

        for pos in line:
            if board_state[pos] == player:
                player_count += 1
            elif board_state[pos] == 0:  # Empty
                empty_count += 1

        # Potential mill: 2 player pieces and 1 empty spot
        if player_count == 2 and empty_count == 1:
            potential_mills += 1

    return potential_mills


def evaluate_positions(current_state, player, opponent):
    """
    Evaluate piece positioning. Central and corner positions have different values.
    """
    score = 0
    board_state = current_state.get_state()

    # Define position values (central positions are more valuable)
    position_values = {
        # High value - central positions that are part of multiple mills
        4: 3, 10: 3, 13: 3, 19: 3,
        # Medium value - other positions
        1: 2, 7: 2, 9: 2, 11: 2, 14: 2, 18: 2, 20: 2, 22: 2,
        # Lower value - corner positions
        0: 1, 2: 1, 3: 1, 5: 1, 6: 1, 8: 1, 12: 1, 15: 1, 16: 1, 17: 1, 21: 1, 23: 1
    }

    for pos, value in position_values.items():
        if board_state[pos] == player:
            score += value
        elif board_state[pos] == opponent:
            score -= value

    return score


def evaluate_blocking(current_state, player, opponent):
    """
    Evaluate how well the player is blocking opponent's potential mills.
    """
    blocking_score = 0
    board_state = current_state.get_state()

    # Define mill lines
    mill_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [9, 10, 11], [12, 13, 14], [15, 16, 17],
        [18, 19, 20], [21, 22, 23],
        [0, 9, 21], [3, 10, 18], [6, 11, 15],
        [1, 4, 7], [16, 19, 22], [8, 12, 17],
        [5, 13, 20], [2, 14, 23]
    ]

    for line in mill_lines:
        opponent_count = 0
        player_count = 0
        empty_count = 0

        for pos in line:
            if board_state[pos] == opponent:
                opponent_count += 1
            elif board_state[pos] == player:
                player_count += 1
            else:
                empty_count += 1

        # Bonus for blocking opponent's potential mill
        if opponent_count == 2 and player_count == 1:
            blocking_score += 20
        # Bonus for having a piece in opponent's potential mill line
        elif opponent_count == 1 and player_count == 1:
            blocking_score += 5

    return blocking_score


def evaluate_phase_bonus(current_state, player, my_phase, opp_phase):
    """
    Provide bonuses based on game phase.
    """
    bonus = 0

    # Phase 1: Placing pieces
    if my_phase == 1:
        # Bonus for having more pieces to place
        pieces_to_place = 9 - current_state.count_pieces(player)
        bonus += pieces_to_place * 2

    # Phase 3: Flying (big advantage)
    if my_phase == 3:
        bonus += 100  # Flying is a significant advantage
    elif opp_phase == 3:
        bonus -= 100  # Opponent flying is bad for us

    # Phase 2: Moving pieces - check if we're constrained
    if my_phase == 2:
        mobility = len(current_state.legal_moves(player))
        if mobility <= 2:  # Very constrained
            bonus -= 50
        elif mobility <= 4:  # Somewhat constrained
            bonus -= 20

    return bonus


def minimax(current_state, current_player, maximizing, depth, visited_states=None, alpha=-INF, beta=INF):
    if visited_states is None:
        visited_states = set()

    state_hash = get_state_hash(current_state)

    if state_hash in visited_states:
        return 0
    else:
        visited_states.add(state_hash)

    terminal_reward = INF - depth

    if current_state.game_over():  # game over
        return -terminal_reward if maximizing else terminal_reward

    if depth == MAX_DEPTH:
        return evaluate_state(current_state, current_player)

    opponent = 3 - current_player
    best_score = -INF if maximizing else INF
    legal_moves = current_state.legal_moves(current_player)

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


def optimal_move(current_state, current_player):
    best_score, best_move, opponent = -INF, None, 3 - current_player
    legal_moves = current_state.legal_moves(player=current_player)

    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(current_player, move)
        score = minimax(next_state, opponent, False, 1)

        if score > best_score:
            best_score, best_move = score, move

    return best_move


env = mill.env(render_mode="human")
env.reset()

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if truncation:
        print("The game was too long!")
        break

    state = mill.transition_model(env)
    player = 1 if agent == "player_1" else 2
    optimal_move = optimal_move(state, player)
    env.step(optimal_move)
