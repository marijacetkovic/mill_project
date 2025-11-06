from famnit_gym.envs import mill
from minimax_implementations import alpha_beta_move_ordering_hashing


# PRECOMPUTE THE BOARD, ACCORDING TO THE SETUP MOVES
def setup_predefined_board(start_env, setup):
    start_env.reset()
    for mv in setup:
        start_env.step(mv)
    return start_env


# SETUP MOVES
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
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
    [1, 10, 0],
    [6, 14, 0],
    [10, 1, 0],
    [14, 6, 0],
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
    [21, 14, 0],
    [23, 24, 0],
    [14, 21, 7],
    [18, 17, 0],
    [21, 14, 0],
    [24, 21, 0],
    [4, 7, 0],
    [17, 18, 10],
    [7, 8, 0],
    [18, 17, 0],
    [19, 11, 0],
    [9, 6, 0],
    [11, 12, 0],
    [6, 3, 0],
    [12, 11, 0],
    [3, 2, 0],
    [11, 12, 0],
    [2, 1, 0],
    [12, 11, 0],
    [1, 10, 0],
    [11, 12, 0],
    [10, 11, 0],
]

# INITIALIZE ENVIRONMENT AND PRECOMPUTE THE STATE
env = setup_predefined_board(mill.env(render_mode="ansi"), setup_moves)
precomputed_state = mill.transition_model(env)
number_of_precomputed_moves = len(setup_moves)
current_player = number_of_precomputed_moves % 2 + 1

# GAME SETUP
ai_player_1 = current_player
ai_player_2 = 3 - ai_player_1
ai_moves = 0

# INITIAL STATE
print(f"Initial state - Player {current_player}'s turn")
print(f"Number of precomputed moves: {number_of_precomputed_moves}")
print(f"Board state:\n{precomputed_state}")
print("-" * 50)

# GAME LOOP
for agent in env.agent_iter():
    current_player = 1 if agent == "player_1" else 2
    observation, reward, termination, truncation, info = env.last()

    # DRAW
    if truncation:
        print("DRAW!")
        break

    state = mill.transition_model(env)
    if state.game_over():
        print("Game Over!")
        print(f"Final state:\n{state}")
        if state.get_phase(ai_player_1) == 'lost':
            print(f"AI Player {ai_player_2} WON")
        else:
            print(f"AI Player {ai_player_1} WON")
        break

    # AI MOVE SELECTION
    if current_player == ai_player_1:
        move = alpha_beta_move_ordering_hashing.find_optimal_move(
            current_state=state,
            maximizing_player=current_player,
            moves_counter=number_of_precomputed_moves + ai_moves
        )
        print(f"AI Player {current_player} move: {move}")
        ai_moves += 1
    else:
        move = alpha_beta_move_ordering_hashing.find_optimal_move(
            current_state=state,
            maximizing_player=current_player,
            moves_counter=number_of_precomputed_moves + ai_moves
        )
        print(f"AI Player {current_player} move: {move}")
        ai_moves += 1

    env.step(move)
