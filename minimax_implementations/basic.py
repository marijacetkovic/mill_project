INF = 200  # GLOBAL INFINITY - CORRESPONDS TO THE MAXIMAL NUMBER OF MOVES ALLOWED


# RECURSIVE MINIMAX ALGORITHM
def minimax(current_state,
            current_player, maximizing_player,
            state_depth, moves_counter):

    # DRAW CONDITION - MAXIMUM GAME LENGTH REACHED
    if state_depth == 200 - moves_counter:
        return 0

    # DETERMINE IF CURRENT PLAYER IS MAXIMIZING OR MINIMIZING
    maximizing = True if current_player == maximizing_player else False
    terminal_reward = INF - state_depth

    # CHECK FOR GAME OVER CONDITION
    if current_state.game_over():
        return -terminal_reward if maximizing else terminal_reward

    # GET LEGAL MOVES
    legal_moves = current_state.legal_moves(current_player)

    # INITIALIZE BEST SCORE BASED ON PLAYER TYPE
    final_score = -INF if maximizing else INF

    # EVALUATE ALL POSSIBLE MOVES
    for move in legal_moves:
        # SIMULATE THE MOVE ON A CLONED STATE
        next_state = current_state.clone()
        next_state.make_move(current_player, move)

        # RECURSIVELY EVALUATE THE RESULTING POSITION
        score = minimax(
            current_state=next_state,
            current_player=3 - current_player,  # SWITCH PLAYER
            maximizing_player=maximizing_player,
            state_depth=state_depth + 1,
            moves_counter=moves_counter
        )

        # UPDATE BEST SCORE AND ALPHA/BETA VALUES
        if maximizing:
            final_score = max(final_score, score)
        else:
            final_score = min(final_score, score)

    return final_score


# TOP-LEVEL MINIMAX FUNCTION THAT RETURNS THE OPTIMAL MOVE TO MAKE
def find_optimal_move(current_state, maximizing_player, moves_counter):
    best_score, optimal_move = -INF, None

    # GET LEGAL MOVES FOR THE CURRENT PLAYER
    legal_moves = current_state.legal_moves(player=maximizing_player)

    # EVALUATE EACH POSSIBLE MOVE
    for move in legal_moves:
        # SIMULATE THE MOVE
        next_state = current_state.clone()
        next_state.make_move(maximizing_player, move)

        # EVALUATE THE RESULTING POSITION USING MINIMAX
        score = minimax(
            current_state=next_state,
            current_player=3 - maximizing_player,  # SWITCH TO OPPONENT
            maximizing_player=maximizing_player,
            state_depth=1,  # START DEPTH COUNTER
            moves_counter=moves_counter
        )

        # UPDATE BEST MOVE IF A BETTER SCORE IS FOUND
        if score > best_score:
            best_score, optimal_move = score, move

    return optimal_move
