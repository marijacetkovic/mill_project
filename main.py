from ai.ai_player import AIPlayer
from famnit_gym.envs import mill

env = mill.env(render_mode="human")
env.reset()

player1_ai = AIPlayer(player_id=1, difficulty="easy")
player2_ai = AIPlayer(player_id=2, difficulty="medium")

for agent in env.agent_iter():
    obs, reward, termination, truncation, info = env.last()

    if termination:
        print("The game is over.")
        winner = 2 if player == 1 else 1
        print(f"Player {agent} has no legal moves. Winner: Player {winner}")

        break
    if truncation:
        print("The game was too long!")
        break

    state = mill.transition_model(env)
    player = 1 if agent == "player_1" else 2
    ai_player = player1_ai if player == 1 else player2_ai

    move = ai_player.choose_move(state)
    if move is None:
        winner = 2 if player == 1 else 1
        print(f"Player {agent} has no legal moves. Winner: Player {winner}")
        break
    else:
        env.step(move)
