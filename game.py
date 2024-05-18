from typing import Optional
from random import choice

from pprint import pformat

class NPuzzleState:
    def __init__(self, matrix: list[list[int]], parent: Optional['NPuzzleState'] = None):
        self.matrix = matrix
        self.parent = parent
        
        self.grid = len(matrix)
        
        for i, row in enumerate(matrix):
            if 0 not in row:
                continue
            
            self.i = i
            self.j = row.index(0)
            
            break

    def __lt__(self, other):
        return True

    def __str__(self):
        string = ''
        
        string += '[\n'
        for row in self.matrix:
            string += ' ' + str(row) + '\n'
        string += ']'
        
        return string

    def __hash__(self):
        return hash(tuple(item for row in self.matrix for item in row))

    def __eq__(self, other: Optional['NPuzzleState']):
        if other is None:
            return False
        
        return self.matrix == other.matrix
        
    def __ne__(self, other: Optional['NPuzzleState']):
        return not self == other
        
    def is_up_possible(self):
        return self.i != 0

    def up(self):
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j], matrix[self.i - 1][self.j] = matrix[self.i - 1][self.j], matrix[self.i][self.j]
        
        return NPuzzleState(matrix, self)

    def is_down_possible(self):
        return self.i != self.grid - 1
    
    def down(self):
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j], matrix[self.i + 1][self.j] = matrix[self.i + 1][self.j], matrix[self.i][self.j]
        
        return NPuzzleState(matrix, self)

    def is_left_possible(self):
        return self.j != 0

    def left(self):
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j], matrix[self.i][self.j - 1] = matrix[self.i][self.j - 1], matrix[self.i][self.j]
        
        return NPuzzleState(matrix, self)
    
    def is_right_possible(self):
        return self.j != self.grid - 1
    
    def right(self):
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j], matrix[self.i][self.j + 1] = matrix[self.i][self.j + 1], matrix[self.i][self.j]
        
        return NPuzzleState(matrix, self)

    def find(self, value: int):
        for i in range(self.grid):
            for j in range(self.grid):
                if value != self.matrix[i][j]:
                    continue
            
                return i, j

    def expand(self):
        states: list[NPuzzleState] = []
        
        if self.is_left_possible():
            states.append(self.left())
        
        if self.is_right_possible():
            states.append(self.right())
        
        if self.is_up_possible():
            states.append(self.up())
        
        if self.is_down_possible():
            states.append(self.down())
        
        return states
    
    def path(self):
        current = self
        path = [current]
        
        while current.parent is not None:
            current = current.parent
            path.append(current)
        
        path.reverse()
        
        return path
    
    @staticmethod
    def goal(n: int):
        grid = (n + 1) ** 0.5
        
        if grid != int(grid):
            raise ValueError('Invalid n value')
        
        grid = int(grid)
        
        # Create matrix of size n x n
        matrix = [[1 + j + i * grid for j in range(grid)] for i in range(grid)]
        # Create empty space
        matrix[grid - 1][grid - 1] = 0
        
        return NPuzzleState(matrix)

    @staticmethod
    def start(n: int, steps: int = 1000):
        
        state = NPuzzleState.goal(n)
        
        for _ in range(steps):
            state = choice(state.expand())
        
        state.parent = None
        
        return state

    @staticmethod
    def manhattan_distance(start: 'NPuzzleState', goal: 'NPuzzleState'):
        distance = 0
        
        for i1 in range(start.grid):
            for j1 in range(start.grid):
                if start.matrix[i1][j1] == 0:
                    continue
                
                for i2 in range(goal.grid):
                    should_break = False
                    
                    for j2 in range(goal.grid):
                        if start.matrix[i1][j1] == goal.matrix[i2][j2]:
                            should_break = True
                            break
                
                    if should_break:
                        break
                
                distance += abs(i1 - i2) + abs(j1 - j2)
        
        return distance

    @staticmethod 
    def tiles_out_of_place(start: 'NPuzzleState', goal: 'NPuzzleState'):
        counter = 0
        
        for i in range(start.grid):
            for j in range(start.grid):
                if start.matrix[i][j] == 0:
                    continue
                
                if start.matrix[i][j] == goal.matrix[i][j]:
                    continue
                
                counter += 1
                

        return counter