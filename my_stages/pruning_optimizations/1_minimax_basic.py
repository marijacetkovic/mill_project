from famnit_gym.envs import mill


inf = 10000


def minimax(current_state, current_player, maximizing, depth):
    opponent = 3 - current_player
    player_state = current_state.get_phase(current_player)
    opponent_state = current_state.get_phase(opponent)

    terminal_reward = inf - depth

    if player_state == "lost":
        if opponent_state == "lost":  # draw
            return 0
        else:  # current_player loses
            return -terminal_reward if maximizing else terminal_reward

    best_score = -inf if maximizing else inf
    legal_moves = current_state.legal_moves(current_player)
    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(current_player, move)
        score = minimax(next_state,  opponent, not maximizing, depth + 1)

        if maximizing:
            best_score = max(best_score, score)
        else:
            best_score = min(best_score, score)

    return best_score


def optimal_move(current_state, current_player):
    best_score, best_move, opponent = -inf, None, 3 - current_player

    legal_moves = current_state.legal_moves(player=current_player)
    for move in legal_moves:
        subsequent_state = current_state.clone()
        subsequent_state.make_move(current_player, move)

        score = minimax(subsequent_state, opponent, False, 1)
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
    #   Note: The correctness of the move is not checked for performance
    #         reasons. The user should only make moves from the list of
    #         legal moves. Player's turn is also not checked. The same
    #         player can be simulated as making multiple consecutive moves.
    #
    # * game_over()
    #   Return True if one of the player has lost the game.
    #
    # Printing the transition model prints the board state in ASCII.
