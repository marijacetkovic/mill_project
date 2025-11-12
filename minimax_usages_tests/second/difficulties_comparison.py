from minimax_usages_tests.second.ai_player_with_difficulty import AiPlayerWithDifficulty
from famnit_gym.envs import mill
from tabulate import tabulate
import itertools
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output_files')


# BENCHMARK FOR HOW DIFFERENT AI DIFFICULTIES PERFORM AGAINST EACH OTHER
def run_benchmark(difficulties_list, num_games):
    print("AI DIFFICULTY TOURNAMENT BENCHMARK")
    print("=" * 70 + "\n")

    results = {}
    group_results = {
        diff: {'wins': 0, 'draws': 0, 'losses': 0}
        for diff in difficulties_list
    }

    # TOURNAMENT LOOP
    for diff1, diff2 in itertools.combinations(difficulties_list, 2):
        print(f"Running matchup: difficulty: {diff1} (Player 1) vs difficulty: {diff2} (Player 2)")
        print("-" * 70)

        key1 = f"difficulty_{diff1}_player_1_wins"
        key2 = f"difficulty_{diff2}_player_2_wins"
        matchup_key = f"{key1}_vs_{key2}"

        results[matchup_key] = {
            key1: 0,
            key2: 0,
            'draws': 0,
        }

        # ITERATIONS LOOP
        for game in range(1, num_games + 1):
            print(f"  Game {game}/{num_games}")

            env = mill.env()
            env.reset()

            ai1 = AiPlayerWithDifficulty(player_id=1, difficulty=diff1)
            ai2 = AiPlayerWithDifficulty(player_id=2, difficulty=diff2)

            total_moves_in_game = 0

            # GAME LOOP
            for agent in env.agent_iter():
                current_player = 1 if agent == "player_1" else 2
                observation, reward, termination, truncation, info = env.last()

                # SELECT AI TO MOVE AT THE MOMENT, AND THE OPPONENT
                ai = ai1 if current_player == 1 else ai2
                opponent_ai = ai1 if current_player == 2 else ai2

                # DRAW
                if truncation:
                    results[matchup_key]["draws"] += 1
                    group_results[diff1]["draws"] += 1
                    group_results[diff2]["draws"] += 1
                    break

                state = mill.transition_model(env)

                # GAME OVER
                if state.game_over():
                    if state.get_phase(ai.player_id) == 'lost':
                        results[matchup_key][
                            f"difficulty_{opponent_ai.difficulty}_player_{opponent_ai.player_id}_wins"] += 1
                        if ai.difficulty == opponent_ai.difficulty:
                            group_results[opponent_ai.difficulty]['wins'] += 1
                        else:
                            group_results[opponent_ai.difficulty]['wins'] += 1
                            group_results[ai.difficulty]['losses'] += 1
                    break

                # CHOOSE MOVE AND MAKE A STEP
                move = ai.choose_move(state, total_moves_in_game)
                env.step(move)
                total_moves_in_game += 1

        # PRINT STATISTICS PER MATCHUP
        print("-" * 70 + "\n")
        print(f"Matchup results")
        print(f"  {key1}: {results[matchup_key][key1]}")
        print(f"  {key2}: {results[matchup_key][key2]}")
        print(f"  Draws: {results[matchup_key]['draws']}")
        print("-" * 70)

    print("\n" + "=" * 70)
    print("TOURNAMENT SUMMARY")
    print("=" * 70)

    print("\nMATCHUP RESULTS:")
    for matchup, outcome in results.items():
        print(f"\n{matchup}:")
        for key, val in outcome.items():
            print(f"  {key}: {val} / {num_games}")

    print("=" * 70 + "\n")
    print("\nOVERALL PERFORMANCE BY DIFFICULTY:")
    for difficulty, stats in group_results.items():
        total_games_per_diff = stats['wins'] + stats['draws'] + stats['losses']
        win_rate = (stats['wins'] / total_games_per_diff * 100)
        print(f"\n{difficulty.upper()}:")
        print(f"  Wins: {stats['wins']} / {total_games_per_diff} (Win rate: {win_rate:.1f}%)")
        print(f"  Draws: {stats['draws']} / {total_games_per_diff}")
        print(f"  Losses: {stats['losses']} / {total_games_per_diff}")

    # CREATE OUTPUT DIRECTORY IF IT DOESN'T EXIST
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # SAVE AS TABLES TO .md FILE
    output_path = os.path.join(OUTPUT_DIR, 'difficulties_comparison_results.md')
    with open(output_path, 'w') as f:
        f.write("MATCHUP RESULTS:\n")

        # Prepare matchup data for table
        matchup_table_data = []
        for matchup, outcome in results.items():
            # Extract players from matchup key
            players = matchup.replace('difficulty_', '').replace('_vs_', ' vs ').replace('_wins', '')
            row = [players]

            # Add results for each outcome
            for key, val in outcome.items():
                if key != 'draws':
                    row.append(f"{val}/{num_games}")
                else:
                    row.append(f"{val}/{num_games}")

            matchup_table_data.append(row)

        # Create matchup table
        headers = ["Matchup", "PLayer 1 Wins", "PLayer 2 Wins", "Draws"]
        matchup_table = tabulate(matchup_table_data, headers=headers, tablefmt="github")
        f.write(matchup_table + "\n")
        f.write("-" * 84 + '\n')

        # Overall Performance Table
        f.write("OVERALL PERFORMANCE BY DIFFICULTY:\n")

        # Prepare performance data for table
        performance_table_data = []
        for difficulty, stats in group_results.items():
            total_games_per_diff = stats['wins'] + stats['draws'] + stats['losses']
            win_rate = (stats['wins'] / total_games_per_diff * 100)

            performance_table_data.append([
                difficulty.upper(),
                f"{stats['wins']}/{total_games_per_diff}",
                f"{win_rate:.1f}%",
                f"{stats['draws']}/{total_games_per_diff}",
                f"{stats['losses']}/{total_games_per_diff}"
            ])

        # Create performance table
        performance_headers = ["Difficulty", "Wins", "Win Rate", "Draws", "Losses"]
        performance_table = tabulate(performance_table_data, headers=performance_headers,
                                     tablefmt="github")
        f.write(performance_table)

    return results, group_results


# RUN BENCHMARK (expected time to finish ~ 8 hours)
if __name__ == "__main__":
    difficulties = ["apprentice", "adventurer", "knight", "champion", "legend"]
    game_results, performance_stats = run_benchmark(difficulties_list=difficulties,
                                                    num_games=10)
