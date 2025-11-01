
import hashlib


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