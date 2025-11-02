from ai_player import AIPlayer
import gymnasium as gym
from famnit_gym.envs import mill
from famnit_gym.wrappers.mill import UserInteraction

def human_vs_ai(human_player = 1, ai_difficulty = "medium"):
    
    env = mill.env(render_mode='human')
    env = UserInteraction(env)
    env.reset()

    ai_player_id = 3 - human_player
    ai = AIPlayer(ai_player_id, difficulty=ai_difficulty)


    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination:
            print(f"{agent} lost the game!")
            break

        if truncation:
            print("The game is too long!")
            break
        
        current_player = 1 if agent == "player_1" else 2

        if current_player == human_player:
            # Let the user decide on the next move.
            move = None
            model = mill.transition_model(env.unwrapped)
            phase = model.get_phase(human_player)

            if phase == 'placing': 
            # Mark all positions to which the player can move a piece.
                for [_, dst, _] in info["legal_moves"]:
                    env.mark_position(dst, (128, 128, 0, 128))  
            else:
                #mark movable pieces
                for [src, _, _] in info["legal_moves"]:
                    env.mark_position(src, (128, 128, 0, 128)) 

            done_interacting = False
            src_selected = None

            while not done_interacting:
                event = env.interact()

                # If the user quit, let us truncate the game.
                if event["type"] == "quit":
                    done_interacting = True
                    truncation = True

                # Use a different selection color for empty and occupied positions.
                elif event["type"] == "mouse_move":
                    if observation[event["position"] - 1] == 0:
                        env.set_selection_color((64, 192, 0, 128))  # Green shade.
                    else:
                        env.set_selection_color((128, 128, 255, 255))  # Blue shade.

                
                elif event["type"] == "mouse_click":
                    pos = event["position"]
                    #placing phase needs only dst
                    if phase == "placing":
                        #if available pos
                        if observation[pos - 1] == 0:
                            #find a legal move w matching dst
                            for [src, dst, capture] in info["legal_moves"]:
                                if dst == pos:
                                    move = [src, dst, capture]
                                    done_interacting = True
                                    break
                    #need src and dst
                    elif phase in ("moving", "flying"):
                        if src_selected is None:
                            # first need to select ur piece
                            if observation[pos - 1] == human_player:
                                src_selected = pos
                                env.clear_markings()
                                # mark where this piece can go
                                for [src, dst, capture] in info["legal_moves"]:
                                    if src == src_selected:
                                        env.mark_position(dst, (128, 128, 0, 128))
                            else:
                                print("You must select your own piece.")
                        else:
                            # second click: select destination
                            for [src, dst, capture] in info["legal_moves"]:
                                if src == src_selected and dst == pos:
                                    move = [src, dst, capture]
                                    done_interacting = True
                                    break
                            src_selected = None
                            env.clear_markings()


                elif event["type"] == "key_press":
                    if event["key"] == "escape":
                        done_interacting = True
                        truncation = True

            env.clear_markings()

            if truncation:
                print("User quit interactively!")
                break
            #need to handle captures!!!!
            
            # Make the chosen move.
            env.step(move)
        else:
            state = mill.transition_model(env.unwrapped)
            move = ai.choose_move(state)
            if move is None:
                print(f"AI player {ai_player_id} has no legal moves. Human wins!")
                break
            env.step(move)


if __name__ == "__main__":
    human_vs_ai(1, "easy")
