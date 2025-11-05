from ai.ai_player import AIPlayer
from famnit_gym.envs import mill
import numpy as np 
import matplotlib.pyplot as plt

difficulties = ["easy", "medium", "hard"]
num_games = 1
results = {}
group_results = {}

# 1 - win , 0 draw, -1 loss
group_results = {
    diff: {1: 0, 0: 0, -1: 0}
    for diff in difficulties
}

#symmetric, counts +1 win +1 loss when same difficulty plays itself
def update_group_results(group_results, winner_diff, loser_diff, draw=False):
    if draw:
        group_results[winner_diff][0] += 1
        #if loser_diff and loser_diff != winner_diff:
        group_results[loser_diff][0] += 1
    else:
        group_results[winner_diff][1] += 1
        #if loser_diff and loser_diff != winner_diff:
        group_results[loser_diff][-1] += 1

for diff1 in difficulties:
    for diff2 in difficulties:
        
        #see if theres advantage to player order
        key1 = diff1 + "_1"
        key2 = diff2 + "_2"
        results[(key1, key2)] = {key1: 0, key2: 0, "draw": 0}
       
        for game in range(1, num_games + 1):
            print(f"\nGame {game}: {key1} vs {key2}")

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
                        print(f"Game over: {key2} wins!")
                        results[(key1, key2)][key2] += 1
                        update_group_results(group_results, diff2, diff1)
                    elif p2_count < 3:
                        print(f"Game over: {key1} wins!")
                        results[(key1, key2)][key1] += 1
                        update_group_results(group_results, diff1, diff2)

                    else:
                        print("Game ended in a draw")
                        results[(key1, key2)]["draw"] += 1
                        update_group_results(group_results, diff1, diff2, draw=True)
                    break

                state = mill.transition_model(env)
                current_player = 1 if agent == "player_1" else 2
                ai = ai1 if current_player == 1 else ai2

                move = ai.choose_move(state)
                if move is None:
                    winner = 2 if current_player == 1 else 1
                    winner_key = key1 if winner == 1 else key2
                    print(f"Player {current_player} has no moves. Winner: {winner_key}")
                    results[(key1, key2)][winner_key] += 1
                    break
                else:
                    env.step(move)

print("\n=== Tournament Results ===")
for (k1, k2), outcome in results.items():
    print(f"{k1} vs {k2}:")
    for key, val in outcome.items():
        print(f"  {key}: {val}")
    print()


labels = list(group_results.keys())

#collect all wins draws losses
#make arrays so we can stack them
wins = np.array([v[1] for v in group_results.values()])
draws = np.array([v[0] for v in group_results.values()])
losses = np.array([v[-1] for v in group_results.values()])

plt.bar(labels, wins, label="Wins")
plt.bar(labels, draws, bottom=wins, label="Draws")
plt.bar(labels, losses, bottom=wins + draws, label="Losses")

plt.ylabel('Number of Games')
plt.xlabel('Difficulty')
plt.title('AI Performance by Difficulty')
plt.legend()

plt.tight_layout()
plt.show()