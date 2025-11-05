from famnit_gym.envs import mill
import hashlib
import time

INF = 201
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


def minimax(current_state, current_player, maximizing_player, maximizing, depth,
            alpha=-INF, beta=INF, visited_states=None):
    global visited_counter, start_time

    if visited_states is None:
        visited_states = set()

    # Compute a hash of the current state
    state_hash = get_state_hash(current_state)

    # If already visited, skip to avoid cycles
    if state_hash in visited_states:
        return 0
    visited_states.add(state_hash)

    # Increment counter and check if it's a multiple of 1,000,000
    visited_counter += 1
    if visited_counter % 1000000 == 0:
        current_time = time.time()
        elapsed_time = current_time - start_time
        nodes_per_second = 1000000 / elapsed_time if elapsed_time > 0 else float('inf')
        print(
            f"Nodes visited: {visited_counter} | Time for last 1M nodes: {elapsed_time:.2f}s | Speed: {nodes_per_second:.0f} nodes/s")
        # Reset start time for the next million
        start_time = current_time

    if depth == 200:  # draw - maximum number of moves reached
        return 0

    terminal_reward = INF - depth

    if current_state.game_over():
        return -terminal_reward if maximizing else terminal_reward

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
    global visited_counter, start_time
    visited_counter = 0  # Reset counter for each move
    start_time = time.time()  # Reset timer for each move
    print("Starting new move search...")

    best_score, best_move = -INF, None
    legal_moves = current_state.legal_moves(player=maximizing_player)

    for move_index, move in enumerate(legal_moves):
        print(f"Evaluating move {move_index + 1}/{len(legal_moves)}: {move}")
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

    return best_move


# ... rest of your code remains the same
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
