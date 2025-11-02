from ai_player import AIPlayer
import gymnasium as gym
from famnit_gym.envs import mill
from famnit_gym.wrappers.mill import UserInteraction

def human_vs_ai(human_player = 1, ai_difficulty = "medium"):
    
    env = mill.env(render_mode='human')
    env = UserInteraction(env)
    env.reset()

    ai_player = 3 - human_player
    ai = AIPlayer(ai_player, difficulty=ai_difficulty)


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

            if truncation:
                print("User quit interactively!")
                break
            
            #if a move is chosen and capturing possible
            if move is not None and move[2] != 0:
                print("Mill possible! Select piece to capture!")
                env.clear_markings()

                #mark all possible captures with chosen src and dst
                for [src, dst, cap] in info["legal_moves"]:
                    if src == move[0] and dst == move[1] and cap != 0:
                        env.mark_position(cap, (255, 64, 64, 128))

                capture_done = False
                while not capture_done:
                    event = env.interact()
                    if event["type"] == "quit":
                        truncation = True
                        capture_done = True
                        break
                    #wait for click
                    elif event["type"] == "mouse_click":
                        pos = event["position"]

                        #if belongs to other player
                        if observation[pos - 1] == ai_player:

                            #find the chosen capture position in legal moves
                            for [src, dst, cap] in info["legal_moves"]:
                                if src == move[0] and dst == move[1] and cap == pos:
                                    #record
                                    move[2] = cap
                                    capture_done = True
                                    break

                env.clear_markings()

            # Make the chosen move.
            env.step(move)
        else:
            state = mill.transition_model(env.unwrapped)
            move = ai.choose_move(state)
            if move is None:
                print(f"AI player {ai_player} has no legal moves. Human wins!")
                break
            env.step(move)


if __name__ == "__main__":
    human_vs_ai(1, "easy")
