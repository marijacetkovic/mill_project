from famnit_gym.envs import mill
import hashlib


INF = 201


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
