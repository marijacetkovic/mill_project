INF = 200  # GLOBAL INFINITY - CORRESPONDS TO THE MAXIMAL NUMBER OF MOVES ALLOWED


# EVALUATES THE CURRENT BOARD STATE AND RETURNS A SCORE FOR THE MOVE
def evaluate_state(current_state, maximizing_player):
    opponent = 3 - maximizing_player
    p1_pieces = current_state.count_pieces(maximizing_player)
    p2_pieces = current_state.count_pieces(opponent)
    piece_advantage = (p1_pieces - p2_pieces) * 30
    position_advantage = evaluate_positions(current_state,
                                            maximizing_player,
                                            opponent)

    # piece_advantage: maximal value is (9 - 2) * 30 = 210, minimal is  -210
    # position_advantage: maximal value is (4 * 8 + 3 * 1) - (3 * 2) = 29, minimal is -29
    # THAT IS WHY 30 IS CHOSEN AS THE MULTIPLICATION FACTOR FOR PIECE ADVANTAGE, SO THAT
    # EVEN IF THERE IS ONE PIECE ADVANTAGE IT IS HIGHER THAN ANY POSITION ADVANTAGE

    # EVALUATE THE TOTAL ADVANTAGE
    evaluated_score = piece_advantage + position_advantage

    # NORMALIZE, SO THAT THE RANGE IS [-1, 1] (this is done so that the true terminating state is
    # always preferred to the heuristically evaluated state)
    normalized_score = evaluated_score / 240
    return normalized_score


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


# RECURSIVE MINIMAX ALGORITHM WITH ALPHA-BETA PRUNING + MOVE ORDERING
def minimax(current_state,
            current_player, maximizing_player,
            state_depth, max_depth,
            moves_counter,
            alpha, beta):
    # DRAW CONDITION - MAXIMUM GAME LENGTH REACHED
    if state_depth == 200 - moves_counter:
        return 0

    # DETERMINE IF CURRENT PLAYER IS MAXIMIZING OR MINIMIZING
    maximizing = True if current_player == maximizing_player else False
    terminal_reward = INF - state_depth

    # CHECK FOR GAME OVER CONDITION
    if current_state.game_over():
        return -terminal_reward if maximizing else terminal_reward

    # CHECK FOR STATES AT MAXIMAL DEPTH
    if state_depth == max_depth:
        return evaluate_state(current_state, maximizing_player)

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
            max_depth=max_depth,
            moves_counter=moves_counter,
            alpha=alpha,
            beta=beta
        )

        # UPDATE BEST SCORE AND ALPHA/BETA VALUES
        if maximizing:
            final_score = max(final_score, score)
            alpha = max(alpha, final_score)
        else:
            final_score = min(final_score, score)
            beta = min(beta, final_score)

        # ALPHA-BETA PRUNING
        if alpha >= beta:
            break

    return final_score


# TOP-LEVEL MINIMAX FUNCTION THAT RETURNS THE OPTIMAL MOVE TO MAKE
def find_optimal_move(current_state, maximizing_player, max_depth, moves_counter):
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
            state_depth=1,
            max_depth=max_depth,
            moves_counter=moves_counter,
            alpha=best_score,  # USE CURRENT BEST AS ALPHA FOR PRUNING
            beta=INF,
        )

        # UPDATE BEST MOVE IF A BETTER SCORE IS FOUND
        if score > best_score:
            best_score, optimal_move = score, move

    return optimal_move
