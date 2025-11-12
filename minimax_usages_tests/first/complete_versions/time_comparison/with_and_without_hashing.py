from famnit_gym.envs import mill
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


# BENCHMARK FOR COMPARISON OF SPEED OF IMPLEMENTATIONS WITH AND WITHOUT HASHING
def run_benchmark(iterations):
    print("WITH vs WITHOUT HASHING BENCHMARK")
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

    ]

    # INITIALIZE ENVIRONMENT AND STATE
    env = mill.env()
    env = setup_predefined_board(start_env=env, setup=setup_moves)
    number_of_precomputed_moves = len(setup_moves)
    precomputed_state = mill.transition_model(env)
    current_player = number_of_precomputed_moves % 2 + 1

    # INITIAL INFORMATION
    print(f"BENCHMARK CONFIGURATION:")
    print("-" * 70)
    print(f"Current Player: {current_player}")
    print(f"Precomputed Moves: {number_of_precomputed_moves}")
    print(f"Iterations: {iterations}")
    print(f"Board State:\n{precomputed_state}")
    print("\n" + "=" * 70)

    # IMPLEMENTATIONS TO TEST
    implementations = [
        ("Alpha-Beta with Move Ordering", alpha_beta_move_ordering.find_optimal_move),
        ("Alpha-Beta with Move Ordering and Hashing", alpha_beta_move_ordering_hashing.find_optimal_move)
    ]

    results = []

    for name, implementation in implementations:
        print(f"\nTesting {name}...")

        total_time = 0.0
        first_move = None

        for i in range(iterations):
            # CREATE A FRESH CLONE
            state_clone = precomputed_state.clone()

            start_time = time.perf_counter()
            optimal_move = implementation(
                current_state=state_clone,
                maximizing_player=current_player,
                moves_counter=number_of_precomputed_moves
            )
            end_time = time.perf_counter()

            computation_time = end_time - start_time
            total_time += computation_time

            # STORE FIRST MOVE
            if i == 0:
                first_move = optimal_move

            # PROGRESS INDICATOR
            if (i + 1) % 10 == 0:
                print(f"  Completed {i + 1}/{iterations} iterations...")

        # CALCULATE AVERAGE TIME
        avg_time = total_time / iterations

        results.append([name, first_move, avg_time])

        print(f"Completed {iterations} iterations for Implementation {name}")

    # DISPLAY COMPARISON RESULTS
    print("\n" + "=" * 70)
    print("\nBENCHMARK RESULTS:")
    print("-" * 70)

    # CREATE TABLE
    console_results = [[name, first_move, f"{avg_time:.4f}s"] for name, first_move, avg_time in results]
    headers = ["Algorithm", "Optimal Move", "Average Computation Time"]
    md_table = tabulate(console_results, headers=headers, tablefmt="github")

    # DISPLAY TABLE
    print(md_table)

    # CALCULATE SPEEDUP
    time1 = results[0][2]
    time2 = results[1][2]

    hashing_speedup = time1 / time2

    if hashing_speedup > 1:
        print(f"Implementation WITH Hashing is {hashing_speedup:.2f}x faster")
    else:
        print(f"Implementation WITHOUT Hashing is {1 / hashing_speedup:.2f}x faster")

    # CREATE OUTPUT DIRECTORY IF IT DOESN'T EXIST
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # SAVE OUTPUT AS A TABLE TO .md file
    output_path = os.path.join(OUTPUT_DIR, 'with_and_without_hashing_benchmark_results.md')

    with open(output_path, 'w') as f:
        f.write("BENCHMARK CONFIGURATION:\n")
        f.write("-" * 70 + "\n")
        f.write(f"Iterations: {iterations}\n")
        f.write(f"Current Player: {current_player}\n")
        f.write(f"Precomputed Moves: {number_of_precomputed_moves}\n")
        f.write(f"Board State:\n{precomputed_state}\n")
        f.write("=" * 70 + "\n")

        f.write(md_table + "\n")
        f.write("-" * 92 + "\n")

        if hashing_speedup > 1:
            f.write(f"Implementation WITH Hashing is {hashing_speedup:.2f}x faster")
        else:
            f.write(f"Implementation WITHOUT Hashing is {1 / hashing_speedup:.2f}x faster")

    return results


# RUN BENCHMARK (expected time to finish ~ 100 minutes)
if __name__ == "__main__":
    benchmark_results = run_benchmark(iterations=100)
