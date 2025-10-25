from famnit_gym.envs import mill
import math


def minimax(model, player, maximizing, depth):
    opponent = 3 - player
    player_state = model._player[player]['phase']
    opponent_state = model._player[opponent]['phase']

    if player_state == "lost":
        if opponent_state == "lost":
            return 0
        else:
            return depth - math.inf
    elif opponent_state == "lost":
        return math.inf - depth

    legal_moves = model.legal_moves(player)
    if maximizing:
        max_value = -math.inf
        for move in legal_moves:
            next_model = model.clone()
            next_model.make_move(player, move)

            value = minimax(next_model, opponent, False, depth + 1)
            max_value = max(max_value, value)
        return max_value

    else:
        min_value = math.inf
        for move in legal_moves:
            next_model = model.clone()
            next_model.make_move(player, move)

            value = minimax(next_model, opponent, True, depth + 1)
            min_value = min(min_value, value)
        return min_value


def ai_move(model, player):
    best_score, best_move = -math.inf, None

    legal_moves = model.legal_moves(player=player)
    for move in legal_moves:
        possible_model = model.clone()
        possible_model.make_move(player, move)

        score = minimax(possible_model, player,False,  1)
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

    player = 1 if agent == "player_1" else 2

    model = mill.transition_model(env)

    move = ai_move(model, player)
    env.step(move)

    # The transition model includes the following public methods:
    # * clone()
    #   Creates a deep copy of the object.
    #
    # * get_state()
    #   Returns the board position as a list [0 - 23], containing values:
    #   0 (empty), 1 (player 1), 2 (player 2).
    #   Note: Board position 1 has index 0 in the list, etc.
    #
    # * get_phase(player)
    #   Returns the phase of the given player (placing, moving, flying).
    #
    # * count_pieces(player)
    #   Returns number of pieces on the board belonging to the given player.
    #
    # * legal_moves(player)
    #   Returns the list of legal moves for the given player.
    #
    # * make_move(player, move)
    #   Changes the state as if the given player made the given move.
    #   Note: The correctnes of the move is not checked for performance
    #         reasons. The user should only make moves from the list of
    #         of legal moves. Player's turn is also not checked. The same
    #         player can be simulated as making multiple consecutive moves.
    #
    # * game_over()
    #   Return True if one of the player has lost the game.
    #
    # Printing the transition model prints the board state in ASCII.
