Stage 1: MiniMax without any optimization ->  Outcome: Maximum recursion depth 
- Observation: Search space is too big.
- Solution: Optimization (1): Alpha-Beta pruning.
---------------------------------------------------------------------------------------------------------------------------------------------
Stage 2:  Minimax with optimization (1) ->  Outcome: Maximum recursion depth 
- Observation: The search space is not finite, because in the second and in the third phase of the game we can do cyclic moves. So the branches that contain at least two exactly equal states (position of the pieces, number of pieces for each player) in the search space can be pruned.
- Solution: Optimization (2): Cutting the branches in the search space that are repeated (the branch is considered repeated if the same state of the board is encountered twice on the same branch)
---------------------------------------------------------------------------------------------------------------------------------------------
Stage 3: MiniMax with Optimization (1) + (2) -> Outcome: Maximum recursion depth 
- Observation: The search space is now finite, but unfeasible, because the cycles can be very large (e.g. the maximal number of configurations of the board with the given number of pieces for each of the players).
- Solution: Optimization (3): Limited depth 
---------------------------------------------------------------------------------------------------------------------------------------------
???Stage 4: MiniMax with optimization (1) + (2) + (3) -> Outcome: Maximum recursion depth 
- Observation:  
- Solution: 
---------------------------------------------------------------------------------------------------------------------------------------------
??? Stage 5: 
- Observation:
- Solution:
---------------------------------------------------------------------------------------------------------------------------------------------
