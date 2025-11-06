from famnit_gym.envs import mill
from minimax_implementations import limited_depth
import time
import random


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

        # COMPUTE FOR THE NUMBER OF ITERATIONS
        for game_iteration in range(iterations_per_depth):

            env = mill.env()
            env.reset()

            ai_player = random.randint(1, 2)
            random_player = 3 - ai_player
            total_moves_in_game = 0

            # ALTERNATE BETWEEN PLAYERS
            for agent in env.agent_iter():
                current_player = 1 if agent == "player_1" else 2
                observation, reward, termination, truncation, info = env.last()

                # DRAW
                if truncation:
                    games_played += 1
                    break

                state = mill.transition_model(env)

                # GAME OVER
                if state.game_over():
                    # AI WON
                    if state.get_phase(random_player) == 'lost':
                        wins += 1
                    games_played += 1
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

                    total_ai_moves += 1
                    total_moves_in_game += 1
                else:
                    # MOVE OF RANDOM PLAYER
                    move = random.choice(state.legal_moves(player=random_player))
                    total_moves_in_game += 1

                env.step(move)

            # PROGRESS INDICATOR
            if (game_iteration + 1) % 10 == 0:
                print(f"  Completed {game_iteration + 1}/{iterations_per_depth} games...")

        # CALCULATE AVERAGES FOR THE DEPTH
        avg_ai_moves_per_game = total_ai_moves / games_played
        avg_time_per_ai_move = total_ai_time / total_ai_moves
        win_rate = (wins / games_played) * 100

        results[max_depth] = {
            'win_rate': win_rate,
            'avg_ai_moves_per_game': avg_ai_moves_per_game,
            'avg_time_per_ai_move': avg_time_per_ai_move
        }

        print(f"\nResults for max_depth = {max_depth}:")
        print(f"  Win Rate: {win_rate:.1f}")
        print(f"  Average Moves per Game: {avg_ai_moves_per_game:.6f}")
        print(f"  Average Time per AI Move: {avg_time_per_ai_move:.6f}s")

    return results


# DEFINE THE MAX DEPTH VALUES TO BE TESTED
max_depth_values = [1, 2, 3, 4]

# RUN BENCHMARK
game_results = run_benchmark(
    max_depth_list=max_depth_values,
    iterations_per_depth=10
)
