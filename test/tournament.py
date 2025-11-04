from ai.ai_player import AIPlayer
from famnit_gym.envs import mill

difficulties = ["easy", "medium", "hard"]
num_games = 1
results = {}

for diff1 in difficulties:
    for diff2 in difficulties:
        results[(diff1, diff2)] = {diff1: 0, diff2: 0, "draw": 0}

        for game in range(1, num_games + 1):
            print(f"\nGame {game}: {diff1} vs {diff2}")

            env = mill.env()
            env.reset()

            ai1 = AIPlayer(player_id=1, difficulty=diff1)
            ai2 = AIPlayer(player_id=2, difficulty=diff2)

            for agent in env.agent_iter():
                obs, reward, done, truncated, info = env.last()

                if done or truncated:
                    state = mill.transition_model(env)
                    p1_count = state.count_pieces(1)
                    p2_count = state.count_pieces(2)

                    if p1_count < 3:
                        print(f"Game over: {diff2} wins!")
                        results[(diff1, diff2)][diff2] += 1
                    elif p2_count < 3:
                        print(f"Game over: {diff1} wins!")
                        results[(diff1, diff2)][diff1] += 1
                    else:
                        print("Game ended in a draw")
                        results[(diff1, diff2)]["draw"] += 1
                    break

                state = mill.transition_model(env)
                current_player = 1 if agent == "player_1" else 2
                ai = ai1 if current_player == 1 else ai2

                move = ai.choose_move(state)
                if move is None:
                    winner = 2 if current_player == 1 else 1
                    winner_diff = diff1 if winner == 1 else diff2
                    print(f"Player {current_player} has no moves. Winner: {winner_diff}")
                    results[(diff1, diff2)][winner_diff] += 1
                    break
                else:
                    env.step(move)

print("\n=== Tournament Results ===")
for (diff1, diff2), outcome in results.items():
    print(f"{diff1} vs {diff2}:")
    for key, val in outcome.items():
        print(f"  {key}: {val}")
    print()
