Stage 1: MiniMax without any optimization -> Minimax with alpha-beta pruning -> Outcome: Maximum recursion depth 
- Observation: The search space is not finite, because in the second phase of the game we can do cyclic moves. So the branches that contain at least two exactly equal states (position of the pieces, number of pieces for each player) in the search space can be pruned.
- Solution: Optimization (1) of cutting the branches in the search space that are repeated (the branch is considered repeated if the same state of the board is encountered twice on the same branch)
---------------------------------------------------------------------------------------------------------------------------------------------
Stage 2: MiniMax with Optimization (1) -> Outcome: ???
---------------------------------------------------------------------------------------------------------------------------------------------
Stage 3: MiniMax with optimization (1) + limited depth of the search + heruistic of number of your pieces - number of pieces of the opponent -> Outcome: ???
---------------------------------------------------------------------------------------------------------------------------------------------


