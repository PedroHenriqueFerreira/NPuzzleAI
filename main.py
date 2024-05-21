from state import *
from search import *

from utils import draw

solvers: dict[str, Search] = {
    'BFS': BreadthFirstSearch(),
    'IDS': IterativeDeepeningSearch(),
    'A_STAR_H1': AStarSearch(NPuzzleState.tiles_out_of_place),
    'A_STAR_H2': AStarSearch(NPuzzleState.manhattan_distance),
    'BIDIRECTIONAL_H1': BidirectionalAStarSearch(NPuzzleState.tiles_out_of_place),
    'BIDIRECTIONAL_H2': BidirectionalAStarSearch(NPuzzleState.manhattan_distance)
}

start = NPuzzleState.start(15, 15)
goal = NPuzzleState.goal(15)

print('-' * 10 + f' START ' + '-' * 10)
print(start)

print('-' * 10 + f' GOAL ' + '-' * 10)
print(goal)

for name in solvers:
    print('-' * 10 + f' {name} ' + '-' * 10)
    
    solver = solvers[name]
    
    solver.search(start, goal)

    print('Passos:', len(solver.path) - 1)
    print('Tempo Gasto:', solver.timer)
    print('Memória Máxima:', solver.memory)
    print('Nós Expandidos:', solver.expanded)
    print('Fator de Ramificação:', solver.branches / solver.expanded if solver.expanded > 0 else 0)

    draw(solver.path)