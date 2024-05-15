from typing import Optional
from random import choice

class NPuzzleState:
    def __init__(self, matrix: list[list[int]]):
        self.n = len(matrix)
        
        self.matrix = matrix
        
        for i, row in enumerate(matrix):
            if 0 not in row:
                continue
            
            self.i = i
            self.j = row.index(0)
            
            break

    def __lt__(self, other):
        return True

    @staticmethod
    def goal(n: int):
        # Create matrix of size n x n
        matrix = [[1 + j + i * n for j in range(n)] for i in range(n)]
        # Create empty space
        matrix[n - 1][n - 1] = 0
        
        return NPuzzleState(matrix)

    @staticmethod
    def manhattan_distance(start: 'NPuzzleState', goal: 'NPuzzleState'):
        distance = 0
        
        for i1 in range(start.n):
            for j1 in range(start.n):
                value = start.matrix[i1][j1]
                
                if value == 0:
                    continue
                
                i2, j2 = goal.find(value)
                
                distance += abs(i1 - i2) + abs(j1 - j2)
        
        return distance

    @staticmethod 
    def tiles_out_of_place(start: 'NPuzzleState', goal: 'NPuzzleState'):
        counter = 0
        
        for i in range(start.n):
            for j in range(start.n):
                if start.matrix[i][j] != goal.matrix[i][j]:
                    if start.matrix[i][j] == 0:
                        continue
                    
                    counter += 1

        return counter

    def random(self, steps: int):
        new = self
        
        for _ in range(steps):
            new = choice(new.expand())

        return new

    def __str__(self):
        lines = []
        
        lines.append('-' * 20)
        
        lines.append(f'N-Puzzle ({self.n} x {self.n})')
        
        for line in self.matrix:
             lines.append(str(line))
            
        lines.append('-' * 20)
            
        return '\n'.join(lines)

    def __hash__(self):
        return hash(tuple(item for row in self.matrix for item in row))

    def __eq__(self, other: Optional['NPuzzleState']):
        if other is None:
            return False
        
        for i, line in enumerate(self.matrix):
            for j, item in enumerate(line):
                if other.find(item) != (i, j):
                    return False
                
        return True
        
    def __ne__(self, other: Optional['NPuzzleState']):
        return not self == other
        
    def is_up_possible(self):
        return self.i != 0

    def up(self):
        value = self.matrix[self.i - 1][self.j]
        
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j] = value
        matrix[self.i - 1][self.j] = 0
        
        return NPuzzleState(matrix)

    def is_down_possible(self):
        return self.i != self.n - 1
    
    def down(self):
        value = self.matrix[self.i + 1][self.j]
        
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j] = value
        matrix[self.i + 1][self.j] = 0
        
        return NPuzzleState(matrix)

    def is_left_possible(self):
        return self.j != 0

    def left(self):
        value = self.matrix[self.i][self.j - 1]
        
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j] = value
        matrix[self.i][self.j - 1] = 0
        
        return NPuzzleState(matrix)
    
    def is_right_possible(self):
        return self.j != self.n - 1
    
    def right(self):
        value = self.matrix[self.i][self.j + 1]
        
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j] = value
        matrix[self.i][self.j + 1] = 0
        
        return NPuzzleState(matrix)

    def find(self, value: int):
        for i in range(self.n):
            for j in range(self.n):
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