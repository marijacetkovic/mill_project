# Minimax Algorithm Seminar Project

This repository contains implementations and tests of the Minimax algorithm with various optimizations, developed for a seminar.

## Repository Structure

### 1. `minimax_implementations/`

This folder contains a series of progressively optimized Minimax implementations.

- **`basic.py`**: The foundational version of Minimax without any optimizations.
- **`alpha_beta.py`**: Extends the basic implementation by adding Alpha-Beta pruning.
- **`alpha_beta_move_ordering.py`**: Enhances the Alpha-Beta implementation by ordering moves to improve pruning efficiency.
- **`alpha_beta_move_ordering_hashing.py`**: Further extends the previous version by caching (hashing) visited game states to prune branches with repeated states.
- **`limited_depth.py`**: Adds a depth limit to the search, building upon all previous optimizations.
- **`for_proof_of_correctness.py`**: A specialized version intended for formal verification of the algorithm's correctness.

### 2. `minimax_usages_tests/`

This folder contains tests and usage examples for the implementations, organized by seminar requirements.

#### Subfolder: `first/`

Contains performance and correctness tests.

- **`complete_versions/`**: Tests for full-depth search implementations.
  - **`time_comparison/`**: Benchmarks the first four implementations in two scenarios:
    1. **`general.py`** Computing an optimal move for an immediate win (4 moves from a draw).
    2. **`with_and_without_hashing.py`** A detailed comparison (100 iterations) between implementations with and without hashing for a deeper scenario (7 moves from a draw).
  - **`proof_of_correctness.py`**: An attempt to validate the algorithm against a known theoretical result. Based on [this paper](https://doi.org/10.1111/j.1467-8640.1996.tb00251.x), which proves a specific game state is a draw with optimal play. If our algorithm finds no winning move from this state, it supports its correctness. *Note: A full run requires searching to depth ~191, which is computationally infeasible (a depth-12 search took ~1 hour).*
- **`limited_versions/`**: Tests for the depth-limited implementation.
  - **`same_depth_comparison/ai_vs_ai_same_depth.py`**: Pit two AI players with the same search depth (1, 2, 3, 4, 5, 6) against each other.
  - **`time_comparison/`**: Measures the time for a depth (1, 2, 3, 4, 5, 6) AI to complete a game against a weaker, partially random opponent (100 trials). Includes a script for generating performance plots.

#### Subfolder: `second/`

Focuses on AI player configurations.

- **`ai_player_with_difficulty.py`**: Implements AI agents with different difficulty levels.
- **`difficulties_comparison.py`**: Runs a round-robin tournament where each difficulty level plays every other level 100 times.

#### Subfolder: `third/`

Provides an interactive game interface.

- **`human_vs_ai_wrapper.py`**: Allows a human player to compete against an AI of a selected difficulty.


## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/marijacetkovic/mill_project.git
cd mill_project
```

### 2. Create a virtual environment:
```bash
python -m venv venv
# Mac/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run scripts

```bash
#Test different complete implementations
python -m minimax_usages_tests.first.complete_versions.time_comparison.general
python -m minimax_usages_tests.first.complete_versions.time_comparison.with_and_without_hashing

#Run proof of correctness
python -m minimax_usages_tests.first.complete_versions.proof_of_correctness

#Limited Depth AI – Same Depth Comparison
python -m minimax_usages_tests.first.limited_version.same_depth_comparison.ai_vs_ai_same_depth

#Limited Depth AI – Different Depth Comparison
python -m minimax_usages_tests.first.limited_version.time_comparison.different_depth_against_base

# AI Difficulty Comparison
python -m minimax_usages_tests.second.difficulties_comparison

# Human vs AI Game
python -m minimax_usages_tests.third.human_vs_ai_wrapper
```
