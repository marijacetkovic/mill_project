import math
from pettingzoo.classic import tictactoe_v3

win_mask = [
    [1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 1, 0, 1, 0, 0]
]

node_count = 0

def opponent(player):
    return (2 if player == 1 else 1)

def make_move(board, move, player):
    new_board = list(board)
    new_board[move] = player
    return new_board

def all_moves(board):
    return [i for (i, x) in enumerate(board) if x == 0]

def board_full(board):
    return 0 not in board

def won(board, player):
    for mask in win_mask:
        player_mask = [m * player for m in mask]
        masked_board = [x * m for (x, m) in zip(board, mask)]
        if masked_board == player_mask:
            return True
    return False

def minimax(board, depth, player, maximizing, alpha=-math.inf, beta=math.inf):
    global node_count
    
    node_count += 1
    reward = 10 - depth

    if won(board, player):
        return reward if maximizing else -reward
    
    if won(board, opponent(player)):
        return -reward if maximizing else reward
    
    if board_full(board):
        return 0
    
    best_score = -math.inf if maximizing else math.inf
    for move in all_moves(board):
        score = minimax(make_move(board, move, player), depth + 1, opponent(player), not maximizing, alpha, beta)

        if maximizing:
            best_score = max(best_score, score)
            alpha = best_score if alpha is None else max(alpha, best_score)
        else:
            best_score = min(best_score, score)
            beta = best_score if beta is None else min(beta, best_score)
        
        if alpha >= beta:
            break

    return best_score

def ai_move(board, player):
    best_score = -math.inf
    best_move = None
    for move in all_moves(board):
        score = minimax(make_move(board, move, player), 0, opponent(player), False)

        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move

env = tictactoe_v3.env(render_mode="human")
env.reset()

board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
game_over = False

for agent in env.agent_iter():
    observation, reward, terminate, truncate, info = env.last()

    if terminate or truncate:
        break

    player = 1 if agent == 'player_1' else 2

    if board == [0, 0, 0, 0, 0, 0, 0, 0, 0]:
        mask = observation["action_mask"]
        move = env.action_space(agent).sample(mask)
    else:
        move = ai_move(board, player)
    
    print("Player", player, "move", move)
    env.step(move)

    board = make_move(board, move, player)

    if won(board, player):
        print("Player", player, "won!")
        break
    
    elif board_full(board):
        print("Draw!")
        break

