from famnit_gym.envs import mill


inf = 1000


def minimax(current_state, current_player, maximizing, depth, alpha=-inf, beta=inf):
    terminal_reward = inf - depth

    if current_state.game_over():  # game over
        return -terminal_reward if maximizing else terminal_reward

    opponent = 3 - current_player
    best_score = -inf if maximizing else inf
    legal_moves = current_state.legal_moves(current_player)

    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(current_player, move)
        score = minimax(next_state, opponent, not maximizing, depth + 1, alpha, beta)

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
    best_score, best_move, opponent = -inf, None, 3 - current_player
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
