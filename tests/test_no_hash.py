from famnit_gym.envs import mill
import time


INF = 200
MOVES_COUNTER = 0


def evaluate_state(current_state, maximizing_player):
    if maximizing_player == 1:
        # Evaluate from Player 1's perspective
        p1_pieces = current_state.count_pieces(1)
        p2_pieces = current_state.count_pieces(2)
        piece_advantage = (p1_pieces - p2_pieces) * 8  # max (9 - 3) * 8 = 48
        position_score = evaluate_positions(current_state, 1, 2)  # max (8 * 4 + 3 - 9*3 = 8)
    else:
        # Evaluate from Player 2's perspective
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
        # Middle Ring
        4: 4, 5: 4, 6: 4, 14: 4, 21: 4, 20: 4, 19: 4, 11: 4,
        # Outer Ring
        1: 3, 2: 3, 3: 3, 15: 3, 24: 3, 23: 3, 22: 3, 10: 3,
        # Inner Ring
        7: 3, 8: 3, 9: 3, 13: 3, 18: 3, 17: 3, 16: 3, 12: 3
    }

    for pos, value in position_values.items():
        if board_state[pos - 1] == player:
            score += value
        elif board_state[pos - 1] == opponent:
            score -= value

    return score


def order_moves(current_state, moves, player, maximizing_player, maximizing):
    move_scores = []
    for move in moves:
        test_state = current_state.clone()
        test_state.make_move(player, move)
        score = evaluate_state(test_state, maximizing_player)
        move_scores.append((move, score))

    # Sort by score (higher is better for maximizing player)
    move_scores.sort(key=lambda x: x[1], reverse=maximizing)

    # Return just the moves in sorted order
    return [move for move, score in move_scores]


def minimax(current_state, current_player, maximizing_player, maximizing, depth,
            alpha=-INF, beta=INF):
    global MOVES_COUNTER

    if depth == 200 - moves_counter:  # draw
        return 0

    terminal_reward = INF - depth

    if current_state.game_over():
        return -terminal_reward if maximizing else terminal_reward

    opponent = 3 - current_player
    best_score = -INF if maximizing else INF
    legal_moves = current_state.legal_moves(current_player)

    ordered_moves = order_moves(current_state, legal_moves, current_player, maximizing_player, maximizing)

    for move in ordered_moves:

        next_state = current_state.clone()
        next_state.make_move(current_player, move)

        score = minimax(
            next_state,
            opponent,
            maximizing_player,
            not maximizing,
            depth + 1,
            alpha,
            beta,
        )

        if maximizing:
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
        else:
            best_score = min(best_score, score)
            beta = min(beta, best_score)

        if alpha >= beta:
            break

    return best_score


def optimal_move(current_state, maximizing_player):
    global MOVES_COUNTER

    best_score, best_move = -INF, None
    legal_moves = current_state.legal_moves(player=maximizing_player)

    ordered_moves = order_moves(current_state, legal_moves, maximizing_player, maximizing_player, True)

    for move in ordered_moves:
        next_state = current_state.clone()
        next_state.make_move(maximizing_player, move)

        score = minimax(
            next_state,
            current_player=3 - maximizing_player,
            maximizing_player=maximizing_player,
            maximizing=False,
            depth=1,
            alpha=best_score,
            beta=INF,
        )

        if score > best_score:
            best_score, best_move = score, move

        print(move, score)
    moves_counter += 1
    return best_move


def setup_predefined_board(env, setup_moves):
    env.reset()
    for move in setup_moves:
        env.step(move)
    return env


setup_moves = [
    [0, 1, 0],
    [0, 4, 0],
    [0, 7, 0],
    [0, 2, 0],
    [0, 5, 0],
    [0, 8, 0],
    [0, 3, 0],
    [0, 6, 0],
    [0, 9, 0],
    [0, 22, 0],
    [0, 19, 0],
    [0, 16, 0],
    [0, 23, 0],
    [0, 20, 0],
    [0, 17, 0],
    [0, 24, 0],
    [0, 21, 0],
    [0, 18, 0],
    [21, 14, 0],
    [22, 10, 0],
    [14, 13, 0],
    [10, 11, 0],
    [19, 22, 0],
    [18, 21, 0],
    [17, 18, 24],
    [16, 19, 1],
    [13, 14, 0],
    [11, 10, 0],
    [14, 13, 2],
    [10, 11, 3],
    [13, 14, 0],
    [11, 10, 0],
    [14, 13, 6],
    [10, 11, 22],
    [13, 14, 0],
    [11, 10, 0],
    [14, 13, 8],
    [10, 11, 5],
    [13, 14, 0],
    [11, 10, 0],
    [14, 13, 4],
    [19, 22, 0],
    [13, 14, 0],
    [22, 19, 7],
    [14, 13, 10],
    [19, 22, 0],
    [9, 8, 0],
    [22, 19, 8],
    [23, 24, 0],
    [19, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
[1, 22, 0],
[24, 23, 0],


]

MOVES_COUNTER = len(setup_moves)
print(MOVES_COUNTER)

env = mill.env()  # Fixed typo: "asci" -> "ascii"
env = setup_predefined_board(env, setup_moves)

observation, reward, termination, truncation, info = env.last()

state = mill.transition_model(env)
player = len(setup_moves) % 2 + 1
print("player", player)
print(state)
print("START OF THE AI")

# Add timer here
start_time = time.time()
optimal_move_result = optimal_move(state, player)
end_time = time.time()

computation_time = end_time - start_time
print(f"AI MOVE: {optimal_move_result}")
print(f"Time needed to compute AI move: {computation_time:.4f} seconds")
env.step(optimal_move_result)
