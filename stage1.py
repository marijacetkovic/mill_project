import gymnasium as gym
from famnit_gym.envs import mill
import math


def get_opponent(player):
    return (2 if player == 1 else 1)


def minimax(model, player, maximizing, alpha=-math.inf, beta=math.inf):
    legal_moves = model.legal_moves(player=player)

    reward = 1
    if model.game_over():
        #game over
        pieces_player = model.count_pieces(player)
        pieces_opponent = model.count_pieces(get_opponent(player))
        reward = pieces_player - pieces_opponent
        return reward if maximizing else -reward

    best_score = -math.inf if maximizing else math.inf
    for move in legal_moves:
        clone = model.clone()
        move_info = clone.make_move(player,move)

        score = minimax(clone, get_opponent(player), not maximizing, depth+1, alpha, beta)

        if maximizing:
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)  
        else:
            best_score = min(best_score, score)
            beta = min(beta, best_score)
        if alpha >= beta:
            break
    

    return best_score


def ai_move(model, player):
    best_score, best_score = -math.inf, None

    legal_moves = model.legal_moves(player=player)
    for move in legal_moves:
        clone = model.clone()
        move_info = clone.make_move(player, move)

        score = minimax(clone, player, True, move_info)
        if score > best_score:
            best_score, best_move = score, move

    return best_move


env = mill.env(render_mode="human")
env.reset()

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    # The game should never terminate, but truncate after 100 moves.
    if truncation:
        print("The game was too long!")
        break

    # Here, we want to do some computations and we need the transition model.
    model = mill.transition_model(env)

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

    # We want to know which player's turn it is.
    player = 1 if agent == "player_1" else 2
    
    # And who is the opponent in this turn.
    opponent = 2 if player == 1 else 1

    # We want to know which player's turn it is.
    player = 1 if agent == "player_1" else 2
    
    # And who is the opponent in this turn.
    opponent = 2 if player == 1 else 1

    move = ai_move(model,player)

    # Make the move that we decided on.
    env.step(move)

