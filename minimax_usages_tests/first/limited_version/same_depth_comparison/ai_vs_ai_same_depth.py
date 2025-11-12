from famnit_gym.envs import mill
from minimax_implementations import limited_depth
from tabulate import tabulate
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output_files')


# BENCHMARK FOR HOW LIMITED DEPTH AI PERFORMS WHEN PLAYING AGAINST THE SAME LIMITED DEPTH AI
def run_benchmark(max_depth_list):
    print("LIMITED DEPTH vs LIMITED DEPTH WITH THE SAME MAX DEPTH BENCHMARK")
    print("=" * 70 + "\n")

    results = {}

    for max_depth in max_depth_list:
        print(f"Running benchmark for max_depth = {max_depth}")

        env = mill.env()
        env.reset()

        total_moves_in_game = 0
        draw = 0
        winner = None

        # ALTERNATE BETWEEN PLAYERS
        for agent in env.agent_iter():
            current_player = 1 if agent == "player_1" else 2
            observation, reward, termination, truncation, info = env.last()

            # DRAW
            if truncation:
                draw = 1
                break

            state = mill.transition_model(env)

            # GAME OVER
            if state.game_over():
                if state.get_phase(current_player) == 'lost':
                    winner = 3 - current_player
                break

            # COMPUTE OPTIMAL MOVE
            move = limited_depth.find_optimal_move(
                current_state=state,
                maximizing_player=current_player,
                max_depth=max_depth,
                moves_counter=total_moves_in_game
            )

            env.step(move)
            total_moves_in_game += 1

        if draw == 1:
            results[max_depth] = {
                'draw': True,
                'total_moves': total_moves_in_game
            }
            print(f"Game ended in a draw after {total_moves_in_game} moves")
        else:
            results[max_depth] = {
                'winner': winner,
                'total_moves': total_moves_in_game
            }
            print(f"Player {winner} won after {total_moves_in_game} moves")

        print("-" * 70)

    print("=" * 70 + "\n")
    print("BENCHMARK SUMMARY:")

    # CREATE TABLE
    console_results = []
    for max_depth, result in results.items():
        if result.get('draw'):
            outcome = "Draw"
        else:
            outcome = f"Player {result['winner']}"
        console_results.append([max_depth, outcome, result['total_moves']])

    headers = ["Maximum Depth", "Winner", "Total Moves"]
    md_table = tabulate(console_results, headers=headers, tablefmt="github")

    # DISPLAY TABLE
    print(md_table)

    # CREATE OUTPUT DIRECTORY IF IT DOESN'T EXIST
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # SAVE OUTPUT AS A TABLE TO .md file
    output_path = os.path.join(OUTPUT_DIR, 'ai_vs_ai_same_depth_results.md')
    with open(output_path, 'w') as f:
        f.write(md_table)

    return results


# RUN BENCHMARK (expected time to finish ~ 100 minutes)
if __name__ == "__main__":
    max_depth_values = [1, 2, 3, 4, 5, 6]
    game_results = run_benchmark(max_depth_values)
