from famnit_gym.envs import mill
from minimax_implementations import basic
from minimax_implementations import alpha_beta
from minimax_implementations import alpha_beta_move_ordering
from minimax_implementations import alpha_beta_move_ordering_hashing
from tabulate import tabulate
import time
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output_files')


# PRECOMPUTE THE BOARD, ACCORDING TO THE SETUP MOVES
def setup_predefined_board(start_env, setup):
    start_env.reset()
    for move in setup:
        start_env.step(move)
    return start_env


# BENCHMARK FOR COMPARISON OF SPEED OF COMPLETE MINIMAX IMPLEMENTATIONS
def run_benchmark():
    print("COMPLETE VERSIONS BENCHMARK")
    print("=" * 70 + "\n")

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
        [1, 22, 0],
        [24, 23, 0],
        [22, 1, 0],
    ]

    # COMPUTE THE NUMBER OF MOVES ALREADY DONE
    number_of_precomputed_moves = len(setup_moves)

    # SET UP THE ENVIRONMENT AND PRECOMPUTE THE BOARD
    env = mill.env()
    env = setup_predefined_board(start_env=env, setup=setup_moves)

    # GET THE STATE, DETERMINE CURRENT PLAYER
    precomputed_state = mill.transition_model(env)
    current_player = len(setup_moves) % 2 + 1

    # CONSIDERED IMPLEMENTATIONS
    implementations = [
        ("Basic Minimax", basic.find_optimal_move),
        ("Alpha-Beta", alpha_beta.find_optimal_move),
        ("Alpha-Beta with Move Ordering", alpha_beta_move_ordering.find_optimal_move),
        ("Alpha-Beta with Move Ordering and Hashing", alpha_beta_move_ordering_hashing.find_optimal_move)
    ]

    # STORE RESULTS IN A LIST
    results = []

    print("BENCHMARK CONFIGURATION:")
    print("-" * 70)
    print(f"Current Player: {current_player}")
    print(f"Precomputed Moves: {number_of_precomputed_moves}")
    print(f"Board State:\n{precomputed_state}")
    print("\n" + "=" * 70)

    print("\nBENCHMARK RESULTS:")
    print("-" * 70)

    for name, implementation in implementations:
        start_time = time.time()

        # CREATE A CLONE OF THE PRECOMPUTED STATE, TO DISABLE CACHING
        precomputed_state_clone = precomputed_state.clone()

        # PRODUCE MOVE
        optimal_move = implementation(
            current_state=precomputed_state_clone,
            maximizing_player=current_player,
            moves_counter=number_of_precomputed_moves
        )

        # STORE RESULTS
        end_time = time.time()
        computation_time = end_time - start_time

        results.append([name, optimal_move, computation_time])

    # CREATE TABLE
    console_results = [[name, move, f"{computation_time:.4f}s"] for name, move, computation_time in results]
    headers = ["Algorithm", "Optimal Move", "Computation Time"]
    md_table = tabulate(console_results, headers=headers, tablefmt="github")

    # DISPLAY TABLE
    print(md_table)

    # CREATE OUTPUT DIRECTORY IF IT DOESN'T EXIST
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # SAVE OUTPUT AS A TABLE TO .md file
    output_path = os.path.join(OUTPUT_DIR, 'general_benchmark_results.md')

    with open(output_path, 'w') as f:
        f.write("BENCHMARK CONFIGURATION:\n")
        f.write("-" * 70 + "\n")
        f.write(f"Current Player: {current_player}\n")
        f.write(f"Precomputed Moves: {number_of_precomputed_moves}\n")
        f.write(f"Board State:\n{precomputed_state}\n")
        f.write("=" * 70 + "\n")

        f.write(md_table + "\n")

    return results


# RUN BENCHMARK (expected time to finish ~20 minutes)
if __name__ == "__main__":
    run_benchmark()
