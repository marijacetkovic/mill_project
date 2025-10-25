from famnit_gym.envs import mill
import math
import hashlib


def get_state_hash(model):
    state_data = (
        model.get_state(),
        model._player[1]['phase'],
        model._player[2]['phase'],
        model._player[1]['pieces_playing'],
        model._player[2]['pieces_playing'],
    )
    return hashlib.md5(str(state_data).encode()).hexdigest()


def minimax(model, move_info, player, maximizing, depth, visited_states=None, alpha=-math.inf, beta=math.inf):
    if visited_states is None:
        visited_states = set()

    state_hash = get_state_hash(model)

    if state_hash in visited_states:
        return 0
    else:
        visited_states.add(state_hash)

    opponent = 3 - player
    player_state = model._player[player]['phase']
    opponent_state = model._player[opponent]['phase']
    print(model, move_info)

    if player_state == "lost":
        if opponent_state == "lost":
            return 0
        else:
            return -1000 + depth
    elif opponent_state == "lost":
        return 1000 - depth

    legal_moves = model.legal_moves(player)
    if maximizing:
        max_value = -math.inf
        for move in legal_moves:
            next_model = model.clone()
            move_info = next_model.make_move(player, move)

            # Pass alpha and beta down the recursion
            value = minimax(next_model, move_info, opponent, False, depth + 1,
                            visited_states.copy(), alpha, beta)
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break  # Beta cutoff
        return max_value

    else:
        min_value = math.inf
        for move in legal_moves:
            next_model = model.clone()
            move_info = next_model.make_move(player, move)

            # Pass alpha and beta down the recursion
            value = minimax(next_model, move_info, opponent, True, depth + 1,
                            visited_states.copy(), alpha, beta)
            min_value = min(min_value, value)
            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_value


def ai_move(model, player):
    best_score, best_move = -math.inf, None

    legal_moves = model.legal_moves(player=player)
    for move in legal_moves:
        possible_model = model.clone()
        move_info = possible_model.make_move(player, move)

        # Initial alpha–beta window for the first call
        score = minimax(possible_model, move_info, player, False, 1,
                        None, -math.inf, math.inf)
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
