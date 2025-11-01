from famnit_gym.envs import mill
from ai.ai_player import get_optimal_move

env = mill.env(render_mode="human")
env.reset()

for agent in env.agent_iter():
    obs, reward, termination, truncation, info = env.last()

    if termination:
        print("The game is over.")
        break
    if truncation:
        print("The game was too long!")
        break

    state = mill.transition_model(env)
    player = 1 if agent == "player_1" else 2
    move = get_optimal_move(state, player)

    if move is None:
        winner = 2 if player == 1 else 1
        print(f"Player {agent} has no legal moves. Winner: Player {winner}")
        break
    else:
        env.step(move)
