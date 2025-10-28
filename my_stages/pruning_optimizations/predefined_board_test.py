from famnit_gym.envs import mill
import hashlib

MAX_DEPTH = 200
INF = MAX_DEPTH + 1


def get_state_hash(current_state):
    """Generate a unique hash for a game state."""
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
    """Minimax algorithm with alpha-beta pruning and state hashing."""

    if visited_states is None:
        visited_states = set()

    # Compute a hash of the current state
    state_hash = get_state_hash(current_state)

    # If already visited, skip to avoid cycles
    if state_hash in visited_states:
        return 0
    visited_states.add(state_hash)

    if depth == 200:  # draw - maximum number of moves reached
        return 0

    terminal_reward = INF - depth

    if current_state.game_over():
        return -terminal_reward if maximizing else terminal_reward

    print(depth, alpha, beta)
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
            visited_states.copy()  # keep each branch independent
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
    best_score, best_move = -INF, None
    legal_moves = current_state.legal_moves(player=maximizing_player)

    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(maximizing_player, move)

        score = minimax(
            next_state,
            current_player=3 - maximizing_player,
            maximizing_player=maximizing_player,
            maximizing=False,
            depth=1,
        )

        if score > best_score:
            best_score, best_move = score, move

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
]

env = mill.env(render_mode="asci")
env = setup_predefined_board(env, setup_moves)

observation, reward, termination, truncation, info = env.last()

state = mill.transition_model(env)
player = len(setup_moves) % 2 + 1
print("player", player)
print(state)
print("START OF THE AI")

optimal_move_result = optimal_move(state, player)
print("AI MOVE: ", optimal_move_result)
env.step(optimal_move_result)
