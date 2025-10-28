from famnit_gym.envs import mill
import random


MAX_DEPTH = 6
INF = 1000 + MAX_DEPTH


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


def minimax(current_state, current_player, maximizing_player, maximizing, depth, alpha=-INF, beta=INF):
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
        score = minimax(next_state, opponent, maximizing_player, not maximizing, depth + 1, alpha, beta)

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
