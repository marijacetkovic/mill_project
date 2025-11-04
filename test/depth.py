import time
import matplotlib.pyplot as plt
from famnit_gym.envs import mill

from ai.utility import get_state_hash
from ai.evaluations import evaluate_state


node_counter = 0

def minimax_with_counter(current_state, current_player, maximizing_player,
                         maximizing, depth, max_depth, visited_states=None,
                         alpha=-1000, beta=1000):
    global node_counter
    node_counter += 1

    if visited_states is None:
        visited_states = set()

    state_hash = get_state_hash(current_state)
    if state_hash in visited_states:
        return 0
    visited_states.add(state_hash)

    # Check for terminal state
    if current_state.game_over():
        terminal_reward = 1000 - depth
        return -terminal_reward if maximizing else terminal_reward

    # Depth limit reached
    if depth >= max_depth:
        return evaluate_state(current_state, maximizing_player)
    

    opponent = 3 - current_player
    best_score = -1000 if maximizing else 1000
    legal_moves = current_state.legal_moves(current_player)

    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(current_player, move)

        score = minimax_with_counter(
            next_state,
            opponent,
            maximizing_player,
            not maximizing,
            depth + 1,
            max_depth,
            visited_states.copy(),
            alpha,
            beta
        )

        if maximizing:
            if score > best_score:
                best_score = score
            if score > alpha:
                alpha = score
        else:
            if score < best_score:
                best_score = score
            if score < beta:
                beta = score

        if beta <= alpha:
            break

    return best_score


max_depths = list(range(0, 8))  
times = []
scores = []
nodes = []

env = mill.env(render_mode="ansi")
env.reset()
initial_state = mill.transition_model(env)  

for depth in max_depths:
    node_counter = 0

    start = time.time()
    
    score = minimax_with_counter(initial_state, current_player=1,
                                 maximizing_player=1, maximizing=True,
                                 depth=0, max_depth=depth)
    
    elapsed = time.time() - start

    times.append(elapsed)
    scores.append(score)
    nodes.append(node_counter)


plots = [
    ("Time (s)", times, "Search Time vs Max Depth", "o", "blue"),
    ("Minimax Value", scores, "Value vs Max Depth", "o", "orange"),
    ("Nodes Visited", nodes, "Nodes Visited vs Max Depth", "o", "green")
]

for ylabel, ydata, title, marker, color in plots:
    plt.figure(figsize=(6,4))
    plt.plot(max_depths, ydata, marker=marker, color=color)
    plt.xlabel("Max Depth")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()