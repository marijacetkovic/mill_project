from famnit_gym.envs import mill
import time


INF = 200  # GLOBAL INFINITY - CORRESPONDS TO THE MAXIMAL NUMBER OF MOVES ALLOWED
MOVES_COUNTER = 0  # GLOBAL MOVE COUNTER - NUMBER OF MOVES ALREADY DONE


# EVALUATES THE CURRENT BOARD STATE AND RETURNS A SCORE FOR THE MOVE
def evaluate_state(current_state, maximizing_player):
    if maximizing_player == 1:
        p1_pieces = current_state.count_pieces(1)
        p2_pieces = current_state.count_pieces(2)
        piece_advantage = (p1_pieces - p2_pieces) * 8
        position_evaluation = evaluate_positions(current_state, 1, 2)
    else:
        p1_pieces = current_state.count_pieces(1)
        p2_pieces = current_state.count_pieces(2)
        piece_advantage = (p2_pieces - p1_pieces) * 8
        position_evaluation = evaluate_positions(current_state, 2, 1)

    evaluated_score = piece_advantage + position_evaluation
    return evaluated_score


# EVALUATES BOARD POSITIONS BY ASSIGNING VALUES TO STRATEGIC POSITIONS
def evaluate_positions(current_state, current_player, opponent):
    evaluated_score = 0
    board_state = current_state.get_state()

    # POSITION VALUES REPRESENT STRATEGIC IMPORTANCE OF EACH BOARD POSITION
    position_values = {
        4: 4, 5: 4, 6: 4, 14: 4, 21: 4, 20: 4, 19: 4, 11: 4,
        1: 3, 2: 3, 3: 3, 15: 3, 24: 3, 23: 3, 22: 3, 10: 3,
        7: 3, 8: 3, 9: 3, 13: 3, 18: 3, 17: 3, 16: 3, 12: 3
    }

    # ADD VALUE FOR PLAYER'S PIECES, SUBTRACT FOR OPPONENT'S PIECES
    for pos, value in position_values.items():
        if board_state[pos - 1] == current_player:
            evaluated_score += value
        elif board_state[pos - 1] == opponent:
            evaluated_score -= value

    return evaluated_score


# ORDERS MOVES BASED ON THEIR EVALUATED SCORES FOR BETTER ALPHA-BETA PRUNING
def order_moves(current_state, current_player, maximizing_player, unordered_moves):
    move_scores = []
    maximizing = True if current_player == maximizing_player else False

    # EVALUATE EACH MOVE BY SIMULATING IT AND SCORING THE RESULTING STATE
    for move in unordered_moves:
        cloned_state = current_state.clone()
        cloned_state.make_move(current_player, move)
        score = evaluate_state(cloned_state, maximizing_player)
        move_scores.append((move, score))

    # SORT MOVES BY SCORE (DESCENDING FOR MAXIMIZING, ASCENDING FOR MINIMIZING)
    move_scores.sort(key=lambda x: x[1], reverse=maximizing)

    return [move for move, score in move_scores]


# RECURSIVE MINIMAX ALGORITHM WITH ALPHA-BETA PRUNING
def minimax(current_state,
            current_player, maximizing_player,
            state_depth, alpha=-INF, beta=INF):
    global MOVES_COUNTER

    # DRAW CONDITION - MAXIMUM GAME LENGTH REACHED
    if state_depth == 200 - MOVES_COUNTER:
        return 0

    # DETERMINE IF CURRENT PLAYER IS MAXIMIZING OR MINIMIZING
    maximizing = True if current_player == maximizing_player else False
    terminal_reward = INF - state_depth

    # CHECK FOR GAME OVER CONDITION
    if current_state.game_over():
        return -terminal_reward if maximizing else terminal_reward

    # GET AND ORDER LEGAL MOVES FOR BETTER PRUNING EFFICIENCY
    legal_moves = current_state.legal_moves(current_player)
    ordered_moves = order_moves(current_state=current_state,
                                current_player=current_player,
                                maximizing_player=maximizing_player,
                                unordered_moves=legal_moves)

    # INITIALIZE BEST SCORE BASED ON PLAYER TYPE
    final_score = -INF if maximizing else INF

    # EVALUATE ALL POSSIBLE MOVES
    for move in ordered_moves:
        # SIMULATE THE MOVE ON A CLONED STATE
        next_state = current_state.clone()
        next_state.make_move(current_player, move)

        # RECURSIVELY EVALUATE THE RESULTING POSITION
        score = minimax(
            current_state=next_state,
            current_player=3 - current_player,  # SWITCH PLAYER
            maximizing_player=maximizing_player,
            state_depth=state_depth + 1,
            alpha=alpha,
            beta=beta,
        )

        # UPDATE BEST SCORE AND ALPHA/BETA VALUES
        if maximizing:
            final_score = max(final_score, score)
            alpha = max(alpha, final_score)
        else:
            final_score = min(final_score, score)
            beta = min(beta, final_score)

        # ALPHA-BETA PRUNING - STOP EVALUATING IF BRANCH IS WORSE THAN KNOWN ALTERNATIVE
        if alpha >= beta:
            break

    return final_score


# TOP-LEVEL MINIMAX FUNCTION THAT RETURNS THE OPTIMAL MOVE TO MAKE
def find_optimal_move(current_state, maximizing_player):
    global MOVES_COUNTER

    best_score, optimal_move = -INF, None

    # GET AND ORDER LEGAL MOVES FOR THE CURRENT PLAYER
    legal_moves = current_state.legal_moves(player=maximizing_player)
    ordered_moves = order_moves(current_state=current_state,
                                current_player=maximizing_player,
                                maximizing_player=maximizing_player,
                                unordered_moves=legal_moves)

    # EVALUATE EACH POSSIBLE MOVE
    for move in ordered_moves:
        # SIMULATE THE MOVE
        next_state = current_state.clone()
        next_state.make_move(maximizing_player, move)

        # EVALUATE THE RESULTING POSITION USING MINIMAX
        score = minimax(
            current_state=next_state,
            current_player=3 - maximizing_player,  # SWITCH TO OPPONENT
            maximizing_player=maximizing_player,
            state_depth=1,  # START DEPTH COUNTER
            alpha=best_score,  # USE CURRENT BEST AS ALPHA FOR PRUNING
            beta=INF,
        )

        # UPDATE BEST MOVE IF A BETTER SCORE IS FOUND
        if score > best_score:
            best_score, optimal_move = score, move

    MOVES_COUNTER += 1
    return optimal_move



def setup_predefined_board(env, setup_moves):
    env.reset()
    for move in setup_moves:
        env.step(move)
    return env


setup_moves = [
    [0, 1, 0],
    [0, 4, 0],
    [0, 7, 0],
    [0, 2, 0],
    [0, 5, 0],
    [0, 8, 0],
    [0, 3, 0],
    [0, 6, 0],
    [0, 9, 0],
    [0, 22, 0],
    [0, 19, 0],
    [0, 16, 0],
    [0, 23, 0],
    [0, 20, 0],
    [0, 17, 0],
    [0, 24, 0],
    [0, 21, 0],
    [0, 18, 0],
    [21, 14, 0],
    [22, 10, 0],
    [14, 13, 0],
    [10, 11, 0],
    [19, 22, 0],
    [18, 21, 0],
    [17, 18, 24],
    [16, 19, 1],
    [13, 14, 0],
    [11, 10, 0],
    [14, 13, 2],
    [10, 11, 3],
    [13, 14, 0],
    [11, 10, 0],
    [14, 13, 6],
    [10, 11, 22],
    [13, 14, 0],
    [11, 10, 0],
    [14, 13, 8],
    [10, 11, 5],
    [13, 14, 0],
    [11, 10, 0],
    [14, 13, 4],
    [19, 22, 0],
    [13, 14, 0],
    [22, 19, 7],
    [14, 13, 10],
    [19, 22, 0],
    [9, 8, 0],
    [22, 19, 8],
    [23, 24, 0],
    [19, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
    [24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
    [1, 22, 0],
[24, 23, 0],
    [22, 1, 0],
    [23, 24, 0],
[1, 22, 0],
[24, 23, 0],
[22, 1, 0],
    [23, 24, 0],

]


MOVES_COUNTER = len(setup_moves)
print(MOVES_COUNTER)

env = mill.env()  # Fixed typo: "asci" -> "ascii"
env = setup_predefined_board(env, setup_moves)

observation, reward, termination, truncation, info = env.last()

state = mill.transition_model(env)
player = len(setup_moves) % 2 + 1
print("player", player)
print(state)
print("START OF THE AI")

# Add timer here
start_time = time.time()
optimal_move_result = find_optimal_move(state, player)
end_time = time.time()

computation_time = end_time - start_time
print(f"AI MOVE: {optimal_move_result}")
print(f"Time needed to compute AI move: {computation_time:.4f} seconds")
env.step(optimal_move_result)
