from n_puzzle import NPuzzleState
from solver import Solver

# 10s
# start = NPuzzleState([
#     [6, 3, 0],
#     [7, 8, 5],
#     [2, 4, 1]
# ])

# 300s
# start = NPuzzleState([
#     [2,  3,  4,  9,  5], 
#     [17,  7,  8, 14, 10],
#     [6,  1, 23, 18, 15],
#     [22, 12, 13, 24, 19],
#     [11, 16, 21, 0, 20]
# ])

goal = NPuzzleState.goal(7)
start = goal.random(100)

path, elapsed_time, max_memory, expand_count, expand_factor = Solver.bidirectional_a_star_search(
    start, 
    goal, 
    NPuzzleState.manhattan_distance
)

# response = Solver.a_star_search(start, goal, NPuzzleState.manhattan_distance)
# response = Solver.a_star_search(start, goal, NPuzzleState.tiles_out_of_place)
# response = Solver.iterative_deepening_search(start, goal)
# response = Solver.deep_limited_search(start, goal, 14)
# response = Solver.breadth_first_search(start, goal)

for i, item in enumerate(path):
    print(f'{i}° PASSO')
    print(item)
    
print('Steps:', len(path) - 1)
print('Elapsed time:', elapsed_time)
print('Max memory:', max_memory)
print('Expand count:', expand_count)
print('Expand factor:', expand_factor)