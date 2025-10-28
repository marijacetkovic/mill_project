from famnit_gym.envs import mill
import hashlib
import random


MAX_DEPTH = 3
INF = 1000 + MAX_DEPTH


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
        position_score = evaluate_positions(current_state, 1, 2)  # max ( 8 * 4 + 3 - 9*3 = 8)
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


def minimax(current_state, current_player, maximizing_player, maximizing, depth, visited_states=None, alpha=-INF,
            beta=INF):

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
        return evaluate_state(current_state, maximizing_player)

    opponent = 3 - current_player
    best_score = -INF if maximizing else INF
    legal_moves = current_state.legal_moves(current_player)

    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(current_player, move)
        score = minimax(next_state, opponent, maximizing_player, not maximizing, depth + 1, visited_states.copy(),
                        alpha, beta)

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
        # The opponent becomes the minimizing player, but perspective stays with current_player
        score = minimax(next_state,
                        current_player=3 - maximizing_player,
                        maximizing_player=maximizing_player,
                        maximizing=False,
                        depth=1)

        if score > best_score:
            best_score, best_move = score, move

    return best_move


env = mill.env(render_mode="None")
env.reset()

ai_player = 1
random_player = 3 - ai_player
ai_moves = 0

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
        if state.get_phase(ai_player) == 'lost':
            print("AI lost")
        else:
            print("AI won, moves needed", ai_moves)
        break

    if current_player == ai_player:
        move = optimal_move(state, ai_player)
        print("ai_move", move)
        ai_moves += 1
    else:
        move = random.choice(state.legal_moves(player=random_player))
        print("random_move", move)

    env.step(move)
