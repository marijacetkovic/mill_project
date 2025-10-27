from famnit_gym.envs import mill
import hashlib

inf = 1000
depth_of_first_win = inf


def get_state_hash(current_state):
    state_data = (
        current_state.get_state(),
        current_state.get_phase(1),
        current_state.get_phase(2),
        current_state.count_pieces(1),
        current_state.count_pieces(2),
    )
    return hashlib.md5(str(state_data).encode()).hexdigest()


def evaluate_move_quality(current_state, current_player, move):
    score = 0

    test_state = current_state.clone()
    test_state_info = test_state.make_move(current_player, move)

    opponent = 3 - current_player

    if test_state_info['opponent_phase'] == 'lost':
        score += inf

    if test_state_info['pieces_captured'] == 1:
        score += 10

    current_mobility = len(current_state.legal_moves(current_player))
    opponent_mobility = len(test_state.legal_moves(opponent))
    new_mobility = len(test_state.legal_moves(current_player))
    if new_mobility > current_mobility:
        score += 1
    if opponent_mobility < current_mobility:
        score += 1

    return score


def order_moves(current_state, current_player, moves):
    scored_moves = []
    for move in moves:
        score = evaluate_move_quality(current_state, current_player, move)
        scored_moves.append((score, move))

    scored_moves.sort(key=lambda x: x[0], reverse=True)
    return [move for score, move in scored_moves]


def minimax(current_state, current_player, maximizing, depth, visited_states=None, alpha=-inf, beta=inf):
    global depth_of_first_win

    if depth >= depth_of_first_win:
        return 0

    if visited_states is None:
        visited_states = set()

    state_hash = get_state_hash(current_state)
    if state_hash in visited_states:
        return 0
    else:
        visited_states.add(state_hash)

    opponent = 3 - current_player
    player_state = current_state.get_phase(current_player)

    terminal_reward = inf - depth

    if player_state == "lost":  # current_player loses
        if not maximizing:
            depth_of_first_solution = min(depth_of_first_solution, depth)
        return -terminal_reward if maximizing else terminal_reward

    best_score = -inf if maximizing else inf
    legal_moves = current_state.legal_moves(current_player)

    ordered_moves = order_moves(current_state, current_player, legal_moves)

    for move in ordered_moves:
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
    global depth_of_first_win
    depth_of_first_solution = 10000

    best_score, best_move, opponent = -inf, None, 3 - current_player
    legal_moves = current_state.legal_moves(player=current_player)

    ordered_moves = order_moves(current_state, current_player, legal_moves)

    for move in ordered_moves:  # Use ordered moves
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
