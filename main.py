from n_puzzle import NPuzzleState
from solver import Solver

from time import time

goal = NPuzzleState.goal(4)
start = goal.random(100)

# start = NPuzzleState([
#     [5, 1, 7, 2],
#     [9, 8, 4, 6],
#     [11, 15, 14, 3],
#     [13, -1, 10, 12]
# ])

# start = NPuzzleState([
#     [8, 6, 1],
#     [7, 5, 2]
#     [-1, 4, 3]
# ])

# start = NPuzzleState([
#     [-1, 6, 5],
#     [2, 3, 1],
#     [4, 8, 7]
# ])

# start = NPuzzleState([
#     [-1, 1, 2, 10, 4],
#     [6, 7, 3, 9, 5],
#     [16, 11, 8, 13, 20],
#     [21, 14, 17, 19, 15],
#     [22, 12, 23, 18, 24]
# ])

# start = NPuzzleState([
#     [6, 9, 2, 4],
#     [5, 3, 7, -1],
#     [13, 8, 1, 12],
#     [11, 10, 14, 15]
# ])

def manhattan_distance(start: NPuzzleState, goal: NPuzzleState):
    distance = 0
    
    for i in range(start.n):
        for j in range(start.n):
            value = start.matrix[i][j]
            
            if value == -1:
                continue
            
            i2, j2 = goal.find(value)
            
            distance += abs(i - i2) + abs(j - j2)
    
    return distance

def wrong_peaces(start: NPuzzleState, goal: NPuzzleState):
    wrong = 0
    
    for i in range(start.n):
        for j in range(start.n):
            value = start.matrix[i][j]
            
            if value == -1:
                continue
            
            i2, j2 = goal.find(value)
            
            if i != i2 or j != j2:
                wrong += 1

    return wrong

print(start)
print(goal)

ini = time()

# response = Solver.a_star_search(start, goal, manhattan_distance)
response = Solver.a_star_bidirectional_search(start, goal, manhattan_distance)
# response = Solver.a_star_search(start, goal, wrong_peaces)
# response = Solver.breadth_first_search(start, goal)
# response = Solver.iterative_deepening_search(start, goal)

elapsed = time() - ini

if response:
    for i, item in enumerate(reversed(response)):
        print(f'{i + 1}° PASSO')
        
        print(item)
else:
    print('FALHA')
    
print('Elapsed time:', elapsed)