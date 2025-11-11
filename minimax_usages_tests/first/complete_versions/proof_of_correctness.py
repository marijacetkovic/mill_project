from famnit_gym.envs import mill
from minimax_implementations import for_proof_of_correctness
import time


# PRECOMPUTE THE BOARD, ACCORDING TO THE SETUP MOVES
def setup_predefined_board(start_env, setup):
    start_env.reset()
    for mv in setup:
        start_env.step(mv)
    return start_env


# PROOF OF CORRECTNESS BASED ON THE PAPER IN WHICH THEY COMPUTATIONALLY PROVE THAT
# THE GAME IS A DRAW
def run_proof_of_correctness():
    # SETUP MOVES
    setup_moves = [
        [0, 5, 0],
        [0, 8, 0],
        [0, 11, 0],
        [0, 12, 0],
        [0, 13, 0],
        [0, 14, 0],
        [0, 17, 0],
        [0, 20, 0],
        [0, 21, 0],
    ]

    # INITIALIZE ENVIRONMENT AND PRECOMPUTE THE STATE
    env = setup_predefined_board(mill.env(render_mode=""), setup_moves)
    precomputed_state = mill.transition_model(env)
    number_of_precomputed_moves = len(setup_moves)
    current_player = number_of_precomputed_moves % 2 + 1
    state = mill.transition_model(env)

    # INITIAL STATE
    print(f"Initial state - Player {current_player}'s turn")
    print(f"Number of precomputed moves: {number_of_precomputed_moves}")
    print(f"Board state:\n{precomputed_state}")
    print("-" * 50)

    # AI MOVE SELECTION - SOMEWHAT IMPLEMENTATION OF ITERATIVE DEEPENING,
    # MAXIMAL FEASIBLE DEPTH REACHED ON ONE OF OUR SETUP WAS 12 -> 57 minutes
    '''If you want to run the complete proof, 
    no need for a loop just run d = 200 - number_of_precomputed_moves '''
    for d in range(1, 200 - number_of_precomputed_moves + 1):
        start_time = time.time()
        move = for_proof_of_correctness.find_optimal_move(
            current_state=state,
            maximizing_player=current_player,
            max_depth=d,
            moves_counter=number_of_precomputed_moves
        )
        end_time = time.time()
        elapsed_time = end_time - start_time

        # IF move == 0, IT MEANS THAT AI CAN ONLY GUARANTEE DRAW AT THIS DEPTH OF SEARCH SPACE
        if move == 0:
            print(f"Maximal considered depth is {d}, ai could only guarantee draw at this maximal depth - PROOF")
        else:
            print(f"Maximal considered depth is {d}, ai could guarantee loss or win at this maximal depth - DISPROOF")

        # Display formatted time
        if elapsed_time > 60:
            minutes = elapsed_time / 60
            print(f"Time needed: {minutes:.2f} minutes, {elapsed_time:.2f} seconds")
        else:
            print(f"Time needed: {elapsed_time:.2f} seconds")


# RUN BENCHMARK (expected time to finish ~ unfeasible)
if __name__ == "__main__":
    run_proof_of_correctness()
