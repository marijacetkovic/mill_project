# from by_points.first.complete_versions import proof_of_correctness
from by_points.first.complete_versions.time_comparison import general
from by_points.first.complete_versions.time_comparison import with_and_without_hashing
from by_points.first.limited_version.time_comparison import different_depth_against_random
from by_points.first.limited_version.time_comparison import plot_different_depth_against_random
from by_points.first.limited_version.same_depth_comparison import ai_vs_ai_same_depth
from by_points.second import difficulties_comparison


MAX_DEPTH_VALUES = [1, 2]
DIFFICULTIES = ["easy", "medium"]


"""GENERAL COMMENTS: COMPLETE IMPLEMENTATION REFERS TO THE IMPLEMENTATION WITHOUT LIMITED DEPTH, 
LIMITED REFERS TO IMPLEMENTATION WITH LIMITED DEPTH, IN THIS FILE ALL THE BENCHMARKS AND TESTS ARE 
SYNCHRONIZED"""


# PROOF OF CORRECTNESS IF THE WHOLE CODE TERMINATES, THEN
# THIS IS A GUARANTEED PROOF OF CORRECTNESS OF THE ALGORITHM
# HOWEVER, WE COULD REACH DEPTH 12 / 191 (since this already took 57 minutes)
# proof_of_correctness.run_proof_of_correctness()


# TIME COMPARISON OF ALL COMPLETE IMPLEMENTATIONS (basic, alpha-beta, move ordering, hashing)
# MEASURES TIME NEEDED TO FIND AN OPTIMAL MOVE,
# WHEN THE BOARD IS PRE-SET TO ALLOW ONLY 4 MOVES UNTIL DRAW
# estimated time to finish is ~ 17 minutes
print("RUNNING BENCHMARK: general")
print("*" * 70 + "\n")
general.run_benchmark()
print("FINISHED BENCHMARK: general")
print("*" * 70 + "\n")


# TIME COMPARISON OF COMPLETE IMPLEMENTATION WITH AND WITHOUT HASHING
# MEASURES AVERAGE TIME NEEDED TO FIND AN OPTIMAL MOVE,
# WHEN THE BOARD IS PRE-SET TO ALLOW ONLY 7 MOVES UNTIL DRAW
# estimated time to finish is ~ 100 minutes
print("RUNNING BENCHMARK: with and without hashing")
print("*" * 70 + "\n")
with_and_without_hashing.run_benchmark(iterations=100)
print("FINISHED BENCHMARK: with and without hashing")
print("*" * 70 + "\n")


# TIME COMPARISON + PLOT OF TIME NEEDED TO COMPLETE A GAME,
# FOR DIFFERENT MAXIMUM DEPTH VALUES FOR LIMITED IMPLEMENTATION,
# WHEN PLAYING AGAINST BASE PLAYER THAT LOOKS ONE MOVE AHEAD AND MAKES
# 10 PERCENTS OF THE MOVES RANDOMLY
# estimated time to finish is ~ 70 minutes
print("RUNNING BENCHMARK: different depth against random")
print("*" * 70 + "\n")
different_depth_against_random.run_benchmark(max_depth_list=[1, 2, 3, 4, 5],
                                             iterations_per_depth=100)
plot_different_depth_against_random.plot_benchmark()
print("FINISHED BENCHMARK: different depth against random")
print("*" * 70 + "\n")


# PERFORMANCE COMPARISON (who wins: player 1 or player 2 and in what number of moves)
# OF LIMITED IMPLEMENTATION,
# WHEN COMPETING AGAINST THE SAME MAXIMAL DEPTH VERSION
# estimated time to finish is ~ 65 + ??? (for depth 7) minutes
print("RUNNING BENCHMARK: same maximum depth")
print("*" * 70 + "\n")
ai_vs_ai_same_depth.run_benchmark(max_depth_list=[1, 2, 3, 4, 5, 7])
print("FINISHED BENCHMARK: same maximum depth")
print("*" * 70 + "\n")


# PERFORMANCE COMPARISON (tournament where each difficulty plays with the other)
# OF DIFFERENT DIFFICULTIES
# estimated time to finish is ~ ???
print("RUNNING BENCHMARK: difficulties comparison")
print("*" * 70 + "\n")
difficulties_comparison.run_benchmark(difficulties_list=["easy", "medium", "hard", "unbeatable"],
                                      num_games=100)
print("FINISHED BENCHMARK: difficulties comparison")
print("*" * 70 + "\n")
