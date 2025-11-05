from .ai_player import AIPlayer
from famnit_gym.envs import mill


def main():
    env = mill.env(render_mode="ansi")
    env.reset()

    player1_ai = AIPlayer(player_id=1, difficulty="hard")
    player2_ai = AIPlayer(player_id=2, difficulty="hard")

    for agent in env.agent_iter():
        obs, reward, termination, truncation, info = env.last()

        if termination or truncation:
            if termination:
                print("The game is over.")
            else:
                print("The game was truncated (too long)!")

            # Determine winner based on remaining pieces or other criteria
            state = mill.transition_model(env)
            p1_pieces = state.count_pieces(1)
            p2_pieces = state.count_pieces(2)

            if p1_pieces < 3:
                print(f"Player 2 wins! (Player 1 has only {p1_pieces} pieces)")
            elif p2_pieces < 3:
                print(f"Player 1 wins! (Player 2 has only {p2_pieces} pieces)")
            else:
                print("Game ended in a draw or unknown state")
            break

        state = mill.transition_model(env)
        player = 1 if agent == "player_1" else 2
        ai_player = player1_ai if player == 1 else player2_ai

        move = ai_player.choose_move(state)
        if move is None:
            winner = 2 if player == 1 else 1
            print(f"Player {player} has no legal moves. Winner: Player {winner}")
            break
        else:
            env.step(move)


if __name__ == "__main__":
    main()
