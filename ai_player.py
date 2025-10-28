from famnit_gym.envs import mill
import hashlib


INF = 1000
MAX_DEPTH = 5


def get_state_hash(current_state):
    state_data = (
        current_state.get_state(),
        current_state.get_phase(1),
        current_state.get_phase(2),
        current_state.count_pieces(1),
        current_state.count_pieces(2),
    )

    return hashlib.md5(str(state_data).encode()).hexdigest()

def phase_to_int(phase):
    phase_map = {
        "placing": 1,
        "moving": 2,
        "flying": 3
    }
    return phase_map.get(phase, 0)

def evaluate_state(state, player):
    opponent = 3 - player
    score = 0

    # mill formation
    score += count_mills(state, player) * 300
    score -= count_mills(state, opponent) * 300  # prevent opponent mills

    # potential mill formation
    score += count_potential_mills(state, player) * 100
    score -= count_potential_mills(state, opponent) * 100  

    #piece count
    score += (state.count_pieces(player) - state.count_pieces(opponent)) * 100

    #move advantage
    score += len(state.legal_moves(player)) * 5
    score -= len(state.legal_moves(opponent)) * 5

    return score

def count_mills(state, player):
    count = 0
    for pos in range(1, 25):
        if state._board[pos] == player and state._in_mill(pos):
            count += 1
    return count // 3


def count_potential_mills(state, player):
    potential_mills = 0

    for mill in state.mills:
        player_count = 0
        empty_count = 0

        for pos in mill:
            if state._board[pos] == player:
                player_count += 1
            elif state._board[pos] == 0: 
                empty_count += 1

        if player_count == 2 and empty_count == 1:
            potential_mills += 1

    return potential_mills

def minimax(current_state, current_player, maximizing, depth, visited_states=None, alpha=-INF, beta=INF):
    if visited_states is None:
        visited_states = set()

    state_hash = get_state_hash(current_state)
    terminal_reward = INF - depth

    if state_hash in visited_states:
        return -terminal_reward if maximizing else terminal_reward
    else:
        visited_states.add(state_hash)


    if current_state.game_over():  # game over
        return 0

    if depth == MAX_DEPTH:
        return evaluate_state(current_state, current_player)
    

    opponent = 3 - current_player
    best_score = -INF if maximizing else INF
    legal_moves = current_state.legal_moves(current_player)
    if not legal_moves:
        return -terminal_reward if maximizing else terminal_reward
    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(current_player, move)
        score = minimax(next_state, opponent, not maximizing, depth + 1, visited_states.copy(), alpha, beta)

        if maximizing:
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
        else:
            best_score = min(best_score, score)
            beta = min(beta, best_score)

        if alpha >= beta:
            break

    return best_score


def get_optimal_move(current_state, current_player):
    best_score, best_move, opponent = -INF, None, 3 - current_player
    legal_moves = current_state.legal_moves(player=current_player)
    visited = {get_state_hash(current_state)}
    if not legal_moves:   
        return None
    for move in legal_moves:
        next_state = current_state.clone()
        next_state.make_move(current_player, move)
        score = minimax(next_state, opponent, False, 1, visited.copy())

        if score > best_score:
            best_score, best_move = score, move

    return best_move


env = mill.env(render_mode="human")
env.reset()

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination:
        print("The game is over.")
        print(f"Player {agent} has no legal moves.")
        break 

    if truncation:
        print("The game was too long!")
        break

    state = mill.transition_model(env)
    player = 1 if agent == "player_1" else 2
    optimal_move = get_optimal_move(state, player)
    if optimal_move is None:
        winner = "player_2" if agent == "player_1" else "player_1"
        print(f"Player {agent} has no legal moves.")
        break 
    else:
        env.step(optimal_move)
    