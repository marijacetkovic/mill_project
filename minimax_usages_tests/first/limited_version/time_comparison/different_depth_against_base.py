from famnit_gym.envs import mill
from minimax_implementations import limited_depth
import random
import time
import math
import json
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output_files')


# BENCHMARK FOR PERFORMANCE OF MINIMAX WITH LIMITED DEPTH AGAINST RANDOM PLAYER
def run_benchmark(max_depth_list, iterations_per_depth):
    print("AI vs RANDOM BENCHMARK")
    print("=" * 70)

    results = {}

    # ITERATE THROUGH ALL MAX DEPTH VALUES TO BE TESTED
    for max_depth in max_depth_list:
        print(f"\nTesting max_depth = {max_depth}")
        print("-" * 70)

        # INITIALIZE VALUES USED FOR STATISTICS
        total_ai_moves = 0
        total_ai_time = 0.0
        wins = 0
        games_played = 0

        # LISTS TO STORE INDIVIDUAL DATA POINTS FOR STANDARD DEVIATION
        ai_move_times = []  # Individual AI move computation times
        ai_moves_per_game_list = []  # AI moves count per game

        # COMPUTE FOR THE NUMBER OF ITERATIONS
        for game_iteration in range(iterations_per_depth):

            env = mill.env()
            env.reset()

            ai_player = random.randint(1, 2)
            base_player = 3 - ai_player
            total_moves_in_game = 0
            ai_moves_this_game = 0
            ai_time_this_game = 0.0

            # ALTERNATE BETWEEN PLAYERS
            for agent in env.agent_iter():
                current_player = 1 if agent == "player_1" else 2
                observation, reward, termination, truncation, info = env.last()

                # DRAW
                if truncation:
                    games_played += 1
                    ai_moves_per_game_list.append(ai_moves_this_game)
                    break

                state = mill.transition_model(env)

                # GAME OVER
                if state.game_over():
                    # AI WON
                    if state.get_phase(base_player) == 'lost':
                        wins += 1

                    games_played += 1
                    ai_moves_per_game_list.append(ai_moves_this_game)
                    break

                # COMPUTE OPTIMAL MOVE FOR AI
                if current_player == ai_player:
                    start_time = time.perf_counter()
                    move = limited_depth.find_optimal_move(
                        current_state=state,
                        maximizing_player=ai_player,
                        max_depth=max_depth,
                        moves_counter=total_moves_in_game
                    )
                    end_time = time.perf_counter()

                    # STORE TIME
                    computation_time = end_time - start_time
                    total_ai_time += computation_time
                    ai_time_this_game += computation_time
                    ai_move_times.append(computation_time)

                    total_ai_moves += 1
                    ai_moves_this_game += 1
                    total_moves_in_game += 1
                else:
                    # MOVE OF PLAYER WHO CAL LOOK ONE MOVE AHEAD AND
                    # PERFORMS 10 PERCENTS OF RANDOM MOVES
                    legal_moves = state.legal_moves(base_player)

                    if random.random() <= 0.1:  # RANDOM MOVE
                        move = random.choice(legal_moves)
                    else:  # OPTIMAL MOVE
                        move = limited_depth.find_optimal_move(current_state=state,
                                                               maximizing_player=base_player,
                                                               max_depth=1,
                                                               moves_counter=total_moves_in_game)
                    total_moves_in_game += 1

                env.step(move)

            # PROGRESS INDICATOR
            if (game_iteration + 1) % 10 == 0:
                print(f"  Completed {game_iteration + 1}/{iterations_per_depth} games...")

        # CALCULATE AVERAGES FOR THE DEPTH
        avg_ai_moves_per_game = total_ai_moves / games_played
        avg_time_per_ai_move = total_ai_time / total_ai_moves
        win_rate = (wins / games_played) * 100

        # CALCULATE STANDARD DEVIATIONS
        def calculate_std_dev(data, mean):
            if len(data) <= 1:
                return 0
            variance = sum((x - mean) ** 2 for x in data) / len(data)
            return math.sqrt(variance)

        # STANDARD DEVIATION FOR TIMES OF AI MOVE
        std_time_per_move = calculate_std_dev(ai_move_times,
                                              avg_time_per_ai_move)

        # STANDARD DEVIATION FOR NUMBER OF AI MOVES PER GAME
        std_moves_per_game = calculate_std_dev(ai_moves_per_game_list,
                                               avg_ai_moves_per_game)

        results[max_depth] = {
            'win_rate': win_rate,
            'avg_ai_moves_per_game': round(avg_ai_moves_per_game, 6),
            'std_ai_moves_per_game': round(std_moves_per_game, 6),
            'avg_time_per_ai_move': round(avg_time_per_ai_move, 6),
            'std_time_per_ai_move': round(std_time_per_move, 6)
        }

        print(f"\nResults for max_depth = {max_depth}:")
        print(f"  Win Rate: {win_rate:.1f}%")
        print(f"  Average Moves per Game: {avg_ai_moves_per_game:.6f} ± {std_moves_per_game:.6f}")
        print(f"  Average Time per AI Move: {avg_time_per_ai_move:.6f}s ± {std_time_per_move:.6f}s")

    # CREATE OUTPUT DIRECTORY IF IT DOESN'T EXIST
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # SAVE RESULTS TO JSON
    output_path = os.path.join(OUTPUT_DIR, 'different_depth_against_base_results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    return results


# RUN BENCHMARK (expected time to finish ~ 5 hours)
if __name__ == "__main__":
    max_depth_values = [1, 2, 3, 4, 5, 6]
    game_results = run_benchmark(max_depth_values, iterations_per_depth=100)
