from famnit_gym.envs import mill
import hashlib


INF = 10000
MAX_DEPTH = 3


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
    ## To FILL
    return 0


def minimax(current_state, current_player, maximizing, depth, visited_states=None, alpha=-INF, beta=INF):
    if visited_states is None:
        visited_states = set()

    state_hash = get_state_hash(current_state)

    if state_hash in visited_states:
        return 0
    else:
        visited_states.add(state_hash)

    terminal_reward = INF - depth

    if depth == MAX_DEPTH:
        max_depth_reward = evaluate_state(current_state, current_player)
        return -max_depth_reward if maximizing else max_depth_reward

    if current_state.game_over():  # game over
        return -terminal_reward if maximizing else terminal_reward

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
