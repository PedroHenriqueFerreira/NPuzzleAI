from typing import Optional
from random import choice

class State:
    ''' Classe abstrata que representa um estado de um problema de busca. '''
    
    def __init__(self, parent: Optional['State'] = None):
        self.parent = parent # Estado pai
    
    def __lt__(self, other: 'State'):
        ''' Método de comparação de estados. (Apenas para ordenação em fila de prioridade). '''
        
        return True

    def expand(self) -> list[tuple[int, 'State']]:
        ''' Expande o estado com todos os estados vizinhos possíveis. '''
        
        raise NotImplementedError()

    def path(self):
        ''' Retorna o caminho do estado atual até o estado inicial. '''
        
        current = self
        path = [current]
        
        while current.parent is not None:
            current = current.parent
            path.append(current)
        
        path.reverse()
        
        return path

class NPuzzleState(State):
    ''' Classe que representa um estado de um problema do quebra-cabeça n-puzzle.'''
    
    def __init__(self, matrix: list[list[int]], parent: Optional['NPuzzleState'] = None):
        self.matrix = matrix # Matriz do estado
        self.parent = parent # Estado pai
        
        self.grid = len(matrix) # Tamanho da matriz
        
        for i, row in enumerate(matrix):
            if 0 not in row:
                continue
            
            self.i = i # Posição da linha do espaço vazio
            self.j = row.index(0) # Posição da coluna do espaço vazio
            
            break

    def __str__(self):
        ''' Retorna a representação do estado em string. '''
        
        string = ''
        
        string += '[\n'
        for row in self.matrix:
            string += ' ' + str(row) + ',\n'
        string += ']'
        
        return string

    def __hash__(self):
        ''' Retorna o hash do estado. (Quando usado como chave em um dicionário). '''
        
        return hash(tuple(item for row in self.matrix for item in row))

    def __eq__(self, other: Optional['NPuzzleState']):
        ''' Método de comparação da igualdade de estados. '''
        
        if other is None:
            return False
        
        return self.matrix == other.matrix
    
    def __ne__(self, other: Optional['NPuzzleState']):
        ''' Método de comparação da diferença de estados. '''
        
        return not self == other
        
    def is_up_possible(self):
        ''' Verifica se é possível mover o espaço vazio para cima.'''
        
        return self.i != 0

    def up(self):
        ''' Move o espaço vazio para cima. '''
        
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j], matrix[self.i - 1][self.j] = matrix[self.i - 1][self.j], matrix[self.i][self.j]
        
        return NPuzzleState(matrix, self)

    def is_down_possible(self):
        ''' Verifica se é possível mover o espaço vazio para baixo. '''
        
        return self.i != self.grid - 1
    
    def down(self):
        ''' Move o espaço vazio para baixo. '''
        
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j], matrix[self.i + 1][self.j] = matrix[self.i + 1][self.j], matrix[self.i][self.j]
        
        return NPuzzleState(matrix, self)

    def is_left_possible(self):
        ''' Verifica se é possível mover o espaço vazio para a esquerda.'''
        
        return self.j != 0

    def left(self):
        ''' Move o espaço vazio para a esquerda. '''
        
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j], matrix[self.i][self.j - 1] = matrix[self.i][self.j - 1], matrix[self.i][self.j]
        
        return NPuzzleState(matrix, self)
    
    def is_right_possible(self):
        ''' Verifica se é possível mover o espaço vazio para a direita. '''
        
        return self.j != self.grid - 1
    
    def right(self):
        ''' Move o espaço vazio para a direita. '''
        
        matrix = [row[:] for row in self.matrix]
        
        matrix[self.i][self.j], matrix[self.i][self.j + 1] = matrix[self.i][self.j + 1], matrix[self.i][self.j]
        
        return NPuzzleState(matrix, self)

    def expand(self):
        states: list[tuple[int, NPuzzleState]] = []
        
        if self.is_up_possible():
            states.append((1, self.up()))
        
        if self.is_down_possible():
            states.append((1, self.down()))
            
        if self.is_left_possible():
            states.append((1, self.left()))
        
        if self.is_right_possible():
            states.append((1, self.right()))
        
        return states
    
    @staticmethod
    def goal(n: int):
        ''' Retorna o estado objetivo de um n-puzzle. '''
        
        grid = (n + 1) ** 0.5
        
        if grid != int(grid):
            raise ValueError('Valor de N inválido.')
        
        grid = int(grid)
        
        # Cria a matriz do estado objetivo
        matrix = [[1 + j + i * grid for j in range(grid)] for i in range(grid)]
        # Criando o espaço vazio
        matrix[grid - 1][grid - 1] = 0
        
        return NPuzzleState(matrix)

    @staticmethod
    def start(n: int, steps: int = 100):
        ''' Retorna um estado inicial aleatório de um n-puzzle. '''
        
        state = NPuzzleState.goal(n)
        
        for i in range(steps):
            states: list[NPuzzleState] = []
            
            for cost, neighbor in state.expand():
                if neighbor in state.path():
                    continue
                
                states.append(neighbor)
            
            if not states:
                print(f'Embaralhamento interrompido em {i} passos')
                break
            
            state = choice(states)
        
        state.parent = None
        
        return state

    def manhattan_distance(self, goal: 'NPuzzleState'):
        ''' Retorna a distância de Manhattan entre o estado e o estado objetivo. '''
        
        distance = 0
        
        for i1 in range(self.grid):
            for j1 in range(self.grid):
                if self.matrix[i1][j1] == 0:
                    continue
                
                for i2 in range(goal.grid):
                    should_break = False
                    
                    for j2 in range(goal.grid):
                        if self.matrix[i1][j1] == goal.matrix[i2][j2]:
                            should_break = True
                            break
                
                    if should_break:
                        break
                
                distance += abs(i1 - i2) + abs(j1 - j2)
        
        return distance

    def tiles_out_of_place(self, goal: 'NPuzzleState'):
        ''' Retorna a quantidade de peças fora do lugar entre o estado e o estado objetivo. '''
        
        counter = 0
        
        for i in range(self.grid):
            for j in range(self.grid):
                if self.matrix[i][j] == 0:
                    continue
                
                if self.matrix[i][j] == goal.matrix[i][j]:
                    continue
                
                counter += 1

        return counter