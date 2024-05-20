from state import *
from search import *

# from utils import draw, write_file

solvers: dict[str, Search] = {
    'BFS': BreadthFirstSearch(),
    'IDS': IterativeDeepeningSearch(),
    'A_STAR_H1': AStarSearch(NPuzzleState.tiles_out_of_place),
    'A_STAR_H2': AStarSearch(NPuzzleState.manhattan_distance),
    'BIDIRECTIONAL_H1': BidirectionalAStarSearch(NPuzzleState.tiles_out_of_place),
    'BIDIRECTIONAL_H2': BidirectionalAStarSearch(NPuzzleState.manhattan_distance)
}

# start = NPuzzleState([
#  [1, 7, 4, 6],
#  [5, 10, 2, 3],
#  [11, 13, 9, 8],
#  [14, 0, 15, 12],
# ])

# start = NPuzzleState.start(15, 10)
start = NPuzzleState([
 [2, 3, 6, 4],
 [1, 5, 7, 8],
 [9, 10, 0, 11],
 [13, 14, 15, 12],
])

goal = NPuzzleState.goal(15)

print('-' * 10 + f' START ' + '-' * 10)
print(start)

print('-' * 10 + f' GOAL ' + '-' * 10)
print(goal)

for name in solvers:
    print('-' * 10 + f' {name} ' + '-' * 10)
    
    solver = solvers[name]
    
    solver.search(start, goal)

    instance = start.flatten()
    steps = len(solver.path) - 1
    timer = solver.timer
    memory = solver.memory
    expanded = solver.expanded
    factor = solver.branches / solver.expanded if solver.expanded > 0 else 0

    # write_file(
    #     'metrics.csv', 
    #     ', '.join([
    #         instance, 
    #         name, 
    #         str(steps), 
    #         f'{timer:.5f}', 
    #         str(memory), 
    #         str(expanded), 
    #         f'{factor:.2f}'
    #     ]) + '\n'
    # )

    print('Passos:', steps)
    print('Tempo Gasto:', timer)
    print('Memória Máxima:', memory)
    print('Nós Expandidos:', expanded)
    print('Fator de Ramificação:', factor)

    # draw(solver.path)