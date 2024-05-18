from game import NPuzzleState
from search import *
from ui import draw

start = NPuzzleState([
    [7, 2, 4],
    [5, 0, 6],
    [8, 3, 1]
])

goal = NPuzzleState([
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
])

solvers: dict[str, Search] = {
    'BFS': BreadthFirstSearch(),
    'IDS': IterativeDeepeningSearch(),
    'A_STAR_H1': AStarSearch(NPuzzleState.tiles_out_of_place),
    'A_STAR_H2': AStarSearch(NPuzzleState.manhattan_distance),
    'BIDIRECTIONAL_A_STAR_H1': BidirectionalAStarSearch(NPuzzleState.tiles_out_of_place),
    'BIDIRECTIONAL_A_STAR_H2': BidirectionalAStarSearch(NPuzzleState.manhattan_distance)
}

print('-' * 10 + f' START ' + '-' * 10)
print(start)

print('-' * 10 + f' GOAL ' + '-' * 10)
print(goal)

for name in solvers:
    if name != 'BIDIRECTIONAL_A_STAR_H2':
        continue
    
    print('-' * 10 + f' {name} ' + '-' * 10)
    
    solver = solvers[name]
    
    solver.search(start, goal)

    for i, state in enumerate(solver.path):
        print(f'STEP {i}')
        print(state)
        print()

    print('STEPS:', len(solver.path) - 1)
    print('ELAPSED TIME:', solver.timer)
    print('MAX MEMORY:', solver.memory)
    print('EXPANDED:', solver.expanded)
    print('FACTOR:', solver.expanded / solver.cycles if solver.cycles > 0 else 0)

    draw(solver.path)