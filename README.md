Stage 1: MiniMax without any optimization ->  Outcome: Maximum recursion depth 
- Observation: Search space is too big.
- Solution: Alpha-Beta pruning.
---------------------------------------------------------------------------------------------------------------------------------------------
Stage 2:  Minimax with alpha-beta pruning ->  Outcome: Maximum recursion depth 
- Observation: The search space is not finite, because in the second phase of the game we can do cyclic moves. So the branches that contain at least two exactly equal states (position of the pieces, number of pieces for each player) in the search space can be pruned.
- Solution: Optimization (1): Cutting the branches in the search space that are repeated (the branch is considered repeated if the same state of the board is encountered twice on the same branch)
---------------------------------------------------------------------------------------------------------------------------------------------
Stage 3: MiniMax with Optimization (1) -> Outcome: Maximum recursion depth 
- Observation: We encounter the goal state in the feasible region of the search space, but since we do not limit the search space, we still reach the limit of the recursion depth.
- Solution: Optimization (2): If the goal state was encountered at the depth d, do not search below - since these goal states are longer to reach, and we are looking for the closest solution
---------------------------------------------------------------------------------------------------------------------------------------------
Stage 4: MiniMax with optimization (1) + (2) -> Outcome: Maximum recursion depth 
- Observation: Feasible search space should now contain the goal state, but since we choose branches "randomly", we can still reach maximum depth of recursion.
- Solution: Optimization (3): Order the branches, so that we are guaranteed to get to the closest solution and then search the whole space up to that level of depth
---------------------------------------------------------------------------------------------------------------------------------------------
Stage 5: MiniMax with optimization (1) + (2) + (3) -> Outcome: The optimal move can be found, but in unfeasible time. E.g. for the stage of the game when the ai needs one move to finish the game, it takes ... ;  when 2 moves are needed, it takes ...
---------------------------------------------------------------------------------------------------------------------------------------------
Stage 6 MiniMax with optimization (1) + limited depth of the search + heruistic of number of your pieces - number of pieces of the opponent -> Outcome: ???


