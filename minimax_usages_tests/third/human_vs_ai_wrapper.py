from minimax_usages_tests.second.ai_player_with_difficulty import AiPlayerWithDifficulty
from famnit_gym.envs import mill
from famnit_gym.wrappers.mill import UserInteraction


# WRAPPER FOR PLAYING AGAINST AI WITH THE SET DIFFICULTY
def human_vs_ai(human_player=1, ai_difficulty="medium"):
    env = mill.env(render_mode='human')
    env = UserInteraction(env)
    env.reset()

    # SET AI PLAYER
    ai_player = 3 - human_player
    ai = AiPlayerWithDifficulty(ai_player, difficulty=ai_difficulty)
    num_moves_already_done = 0

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()
        current_player = 1 if agent == "player_1" else 2
        state = mill.transition_model(env.unwrapped)

        # DRAW
        if truncation:
            print("DRAW!")
            break

        if state.game_over():
            if current_player == human_player:
                print("LOSE!")
                break
            else:
                print("WIN!")
                break

        # USER'S TURN
        if current_player == human_player:
            move = None
            model = mill.transition_model(env.unwrapped)
            phase = model.get_phase(human_player)

            if phase == 'placing':
                # MARK ALL POSITIONS TO WHICH THE PLAYER CAN MOVE A PIECE
                for [_, dst, _] in info["legal_moves"]:
                    env.mark_position(dst, (128, 128, 0, 128))
            else:
                # MARK MOVABLE PIECES
                for [src, _, _] in info["legal_moves"]:
                    env.mark_position(src, (128, 128, 0, 128))

            done_interacting = False
            src_selected = None

            while not done_interacting:
                event = env.interact()

                # IF THE USER QUIT, TRUNCATE THE GAME
                if event["type"] == "quit":
                    done_interacting = True
                    truncation = True

                # USE A DIFFERENT SELECTION COLOR FOR EMPTY AND OCCUPIED POSITIONS
                elif event["type"] == "mouse_move":
                    if observation[event["position"] - 1] == 0:
                        env.set_selection_color((64, 192, 0, 128))
                    else:
                        env.set_selection_color((128, 128, 255, 255))

                elif event["type"] == "mouse_click":
                    pos = event["position"]

                    # PLACING PHASE NEEDS ONLY DST
                    if phase == "placing":
                        # IF AVAILABLE POS
                        if observation[pos - 1] == 0:
                            # FIND A LEGAL MOVE WITH MATCHING DST
                            for [src, dst, capture] in info["legal_moves"]:
                                if dst == pos:
                                    move = [src, dst, capture]
                                    done_interacting = True
                                    break

                    # NEED SRC AND DST
                    elif phase in ("moving", "flying"):
                        if src_selected is None:
                            # FIRST NEED TO SELECT UR PIECE
                            if observation[pos - 1] == human_player:
                                src_selected = pos
                                env.clear_markings()
                                # MARK WHERE THIS PIECE CAN GO
                                for [src, dst, _] in info["legal_moves"]:
                                    if src == src_selected:
                                        env.mark_position(dst, (128, 128, 0, 128))
                            else:
                                print("You must select your own piece.")
                        else:
                            # SECOND CLICK: SELECT DESTINATION
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

            # IF A MOVE IS CHOSEN AND CAPTURING POSSIBLE
            if move is not None and move[2] != 0:
                print("Mill possible! Select piece to capture!")
                env.clear_markings()

                # MARK ALL POSSIBLE CAPTURES WITH CHOSEN SRC AND DST
                for [src, dst, cap] in info["legal_moves"]:
                    if src == move[0] and dst == move[1] and cap != 0:
                        env.mark_position(cap, (255, 64, 64, 128))

                capture_done = False
                while not capture_done:
                    event = env.interact()
                    if event["type"] == "quit":
                        break
                    # WAIT FOR CLICK
                    elif event["type"] == "mouse_click":
                        pos = event["position"]

                        # IF BELONGS TO OTHER PLAYER
                        if observation[pos - 1] == ai_player:

                            # FIND THE CHOSEN CAPTURE POSITION IN LEGAL MOVES
                            for [src, dst, cap] in info["legal_moves"]:
                                if src == move[0] and dst == move[1] and cap == pos:
                                    # RECORD
                                    move[2] = cap
                                    capture_done = True
                                    break

                env.clear_markings()

            # MAKE THE CHOSEN MOVE
            env.step(move)
            num_moves_already_done += 1
        else:
            move = ai.choose_move(current_state=state,
                                  num_moves_already_done=num_moves_already_done)
            env.step(move)
            num_moves_already_done += 1


# RUN THE GAME
if __name__ == "__main__":
    # GET HUMAN PLAYER CHOICE
    while True:
        try:
            player_choice = input("Which player do you want to be? (1 or 2) [default: 1]: ").strip()
            if player_choice == "":
                chosen_human_player = 1
                break
            chosen_human_player = int(player_choice)
            if chosen_human_player in [1, 2]:
                break
            else:
                print("Please enter 1 or 2")
        except ValueError:
            print("Please enter a valid number (1 or 2)")

    # GET DIFFICULTY CHOICE
    difficulties = ["apprentice", "adventurer", "knight", "champion", "legend"]
    while True:
        player_choice_difficulty = input("Choose AI difficulty (apprentice, adventurer, knight, champion {slow}, legend {very slow}) [default: knight]: ").strip().lower()
        if player_choice_difficulty == "":
            chosen_difficulty = "knight"
            break
        if player_choice_difficulty in difficulties:
            chosen_difficulty = player_choice_difficulty
            break
        else:
            print("Please choose from: apprentice, adventurer, knight, champion, legend")

    human_vs_ai(human_player=chosen_human_player,
                ai_difficulty=chosen_difficulty)
