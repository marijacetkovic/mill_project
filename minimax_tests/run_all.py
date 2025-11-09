# from by_points.first.complete_versions import proof_of_correctness
from by_points.first.complete_versions.time_comparison import general
from by_points.first.complete_versions.time_comparison import with_and_without_hashing
from by_points.first.limited_version.time_comparison import different_depth_against_random
from by_points.first.limited_version.time_comparison import plot_different_depth_against_random
from by_points.first.limited_version.same_depth_comparison import ai_vs_ai_same_depth
from by_points.second import difficulties_comparison


MAX_DEPTH_VALUES = [1, 2]
ITERATIONS = 2
DIFFICULTIES = ["easy", "medium"]


"""GENERAL COMMENTS: COMPLETE IMPLEMENTATION REFERS TO THE IMPLEMENTATION WITHOUT LIMITED DEPTH, 
LIMITED REFERS TO IMPLEMENTATION WITH LIMITED DEPTH, IN THIS FILE ALL THE BENCHMARKS AND TESTS ARE 
SYNCHRONIZED"""


# TO DO: proof of correctness

# TIME COMPARISON OF ALL COMPLETE IMPLEMENTATIONS (basic, alpha-beta, move ordering, hashing)
# MEASURES TIME NEEDED TO FIND AN OPTIMAL MOVE,
# WHEN THE BOARD IS PRE-SET TO ALLOW ONLY 4 MOVES UNTIL DRAW
print("RUNNING BENCHMARK: general")
print("*" * 70 + "\n")
general.run_benchmark()
print("FINISHED BENCHMARK: general")
print("*" * 70 + "\n")

# TIME COMPARISON OF COMPLETE IMPLEMENTATION WITH AND WITHOUT HASHING
# MEASURES AVERAGE TIME NEEDED TO FIND AN OPTIMAL MOVE,
# WHEN THE BOARD IS PRE-SET TO ALLOW ONLY 8 MOVES UNTIL DRAW
print("RUNNING BENCHMARK: with and without hashing")
print("*" * 70 + "\n")
with_and_without_hashing.run_benchmark(iterations=ITERATIONS)
print("FINISHED BENCHMARK: with and without hashing")
print("*" * 70 + "\n")

# TIME COMPARISON + PLOT OF TIME NEEDED TO COMPLETE A GAME,
# FOR DIFFERENT MAXIMUM DEPTH VALUES FOR LIMITED IMPLEMENTATION,
# WHEN PLAYING AGAINST RANDOM PLAYER (chooses random move)
print("RUNNING BENCHMARK: different depth against random")
print("*" * 70 + "\n")
different_depth_against_random.run_benchmark(max_depth_list=MAX_DEPTH_VALUES,
                                             iterations_per_depth=ITERATIONS)
plot_different_depth_against_random.plot_benchmark()
print("FINISHED BENCHMARK: different depth against random")
print("*" * 70 + "\n")


# PERFORMANCE COMPARISON (who wins: player 1 or player 2 and in what number of moves)
# OF LIMITED IMPLEMENTATION,
# WHEN COMPETING AGAINST THE SAME MAXIMAL DEPTH VERSION
print("RUNNING BENCHMARK: same maximum depth")
print("*" * 70 + "\n")
ai_vs_ai_same_depth.run_benchmark(max_depth_list=MAX_DEPTH_VALUES)
print("FINISHED BENCHMARK: same maximum depth")
print("*" * 70 + "\n")

# PERFORMANCE COMPARISON (tournament where each difficulty plays with the other)
# OF DIFFERENT DIFFICULTIES
print("RUNNING BENCHMARK: difficulties comparison")
print("*" * 70 + "\n")
difficulties_comparison.run_benchmark(difficulties_list=DIFFICULTIES,
                                      num_games=ITERATIONS)
print("FINISHED BENCHMARK: difficulties comparison")
print("*" * 70 + "\n")
