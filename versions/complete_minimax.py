from famnit_gym.envs import mill
import hashlib
import time

INF = 201
MOVES_COUNTER = 0
visited_counter = 0  # Global counter
start_time = None  # Global start time


def get_state_hash(current_state):
    state_data = (
        current_state.get_state(),
        current_state.get_phase(1),
        current_state.get_phase(2),
        current_state.count_pieces(1),
        current_state.count_pieces(2),
    )
    return hashlib.md5(str(state_data).encode()).hexdigest()


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
    """
    Order moves from best to worst based on quick evaluation.
    For maximizing: best moves first
    For minimizing: worst moves first (from maximizing player's perspective)
    """
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
            alpha=-INF, beta=INF, visited_states=None):
    global visited_counter, start_time, MOVES_COUNTER

    if visited_states is None:
        visited_states = set()

    # Compute a hash of the current state
    state_hash = get_state_hash(current_state)

    # If already visited, skip to avoid cycles
    if state_hash in visited_states:
        return 0
    visited_states.add(state_hash)

    # Increment counter and check if it's a multiple of 1000000
    visited_counter += 1
    if visited_counter % 1000000 == 0:
        current_time = time.time()
        elapsed_time = current_time - start_time
        nodes_per_second = 1000000 / elapsed_time if elapsed_time > 0 else float('inf')
        print(
            f"Nodes visited: {visited_counter} | Time for last 1M nodes: {elapsed_time:.2f}s | Speed: {nodes_per_second:.0f} nodes/s")
        # Reset start time for the next million
        start_time = current_time

    if depth == 200 - moves_counter:  # draw - maximum number of moves reached
        return 0

    terminal_reward = INF - depth

    if current_state.game_over():
        return -terminal_reward if maximizing else terminal_reward

    opponent = 3 - current_player
    best_score = -INF if maximizing else INF
    legal_moves = current_state.legal_moves(current_player)

    # Order moves for better pruning efficiency
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
            visited_states.copy()
        )

        if maximizing:
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
        else:
            best_score = min(best_score, score)
            beta = min(beta, best_score)

        if beta <= alpha:
            break

    return best_score


def optimal_move(current_state, maximizing_player):
    global visited_counter, start_time, MOVES_COUNTER
    visited_counter = 0  # Reset counter for each move
    start_time = time.time()  # Reset timer for each move
    print("Starting new move search...")

    best_score, best_move = -INF, None
    legal_moves = current_state.legal_moves(player=maximizing_player)

    # Order moves for the root node as well
    ordered_moves = order_moves(current_state, legal_moves, maximizing_player, maximizing_player, True)

    for move_index, move in enumerate(ordered_moves):
        print(f"Evaluating move {move_index + 1}/{len(ordered_moves)}: {move}")
        move_start_time = time.time()

        next_state = current_state.clone()
        next_state.make_move(maximizing_player, move)

        score = minimax(
            next_state,
            current_player=3 - maximizing_player,
            maximizing_player=maximizing_player,
            maximizing=False,
            depth=1,
        )

        move_time = time.time() - move_start_time
        print(f"Move {move} evaluated in {move_time:.2f}s with score {score}")

        if score > best_score:
            best_score, best_move = score, move
            print(f"New best move: {best_move} with score {best_score}")

    total_time = time.time() - start_time
    if visited_counter > 0:
        overall_speed = visited_counter / total_time
        print(f"Move completed. Total nodes visited: {visited_counter}")
        print(f"Total time: {total_time:.2f}s | Overall speed: {overall_speed:.0f} nodes/s")

    moves_counter +=1
    return best_move


env = mill.env()
env.reset()

ai_player_1 = 1
ai_player_2 = 3 - ai_player_1
ai_moves_1, ai_moves_2 = 0, 0

for agent in env.agent_iter():
    current_player = 1 if agent == "player_1" else 2
    print(agent)
    observation, reward, termination, truncation, info = env.last()

    if truncation:
        print("The game was too long!")
        break

    state = mill.transition_model(env)

    if state.game_over():
        print("Game over!")
        print(state)
        if state.get_phase(ai_player_1) == 'lost':
            print("Second AI Won, moves needed", ai_moves_2)
        else:
            print("First AI won, moves needed", ai_moves_1)
        break

    if current_player == ai_player_1:
        move = optimal_move(state, ai_player_1)
        print("ai_move_1", move)
        ai_moves_1 += 1
    else:
        move = optimal_move(state, ai_player_2)
        print("ai_move_2", move)
        ai_moves_2 += 1

    env.step(move)
