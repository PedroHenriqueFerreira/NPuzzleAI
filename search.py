from typing import Callable, Optional
from time import time

from structure import *

from state import State

class Search:
    ''' Classe abstrata que define um algoritmo de busca '''
    
    def __init__(self):
        self.timer = 0 # Tempo levado para executar o algoritmo
        
        self.memory = 0 # Uso máximo de memória do algoritmo
        self.expanded = 0 # Número de nós expandidos
        self.branches = 0 # Número de ramificações do algoritmo
        
        self.is_done = False # Se o algoritmo está finalizado
        
        self.current: Optional[State] = None # Estado atual do algoritmo
        
        self.structure: Optional[Structure] = None # Estrutura de dados do algoritmo
        
        self.path: list[State] = [] # Solução encontrada pelo algoritmo
        
    def clear(self):
        ''' Reinicia as variáveis do algoritmo '''
        
        self.timer = time()
        
        self.memory = 0
        self.expanded = 0
        self.branches = 0
        
        self.is_done = False
        
        self.current = None
        
        self.structure = None
        
        self.path.clear()
        
    def update_timer(self):
        ''' Finaliza o cronômetro do algoritmo '''
        
        self.timer = time() - self.timer

    def update_memory(self, *structures: Structure):
        ''' Atualiza o uso máximo de memória do algoritmo '''
        
        if structures:
            self.memory = max(self.memory, sum(structure.size() for structure in structures))
        else:
            if self.structure is None:
                return
            
            self.memory = max(self.memory, self.structure.size())

    def update_expanded(self, *values: int):
        ''' Atualiza o número de nós expandidos '''
        
        if values:
            self.expanded += sum(values)
        else:
            self.expanded += 1

    def update_branches(self, *values: int):
        ''' Atualiza o número de ramificações do algoritmo '''
        
        if values:
            self.branches += sum(values)
        else:
            self.branches += 1
        
    def update_done(self):
        ''' Finaliza o algoritmo '''
        
        self.is_done = True
        
    def update_path(self, *paths: list[State]):
        ''' Atualiza a solução encontrada pelo algoritmo '''
        
        if paths:
            for path in paths:
                self.path.extend(path)
        else:
            self.path.extend(self.current.path())

    def search(self, start: State, goal: State):
        ''' Executa o algoritmo de busca '''
        
        raise NotImplementedError()

class BreadthFirstSearch(Search):
    ''' Algoritmo de busca em largura '''
    
    def __init__(self):
        super().__init__()
        
        self.closed_set: set[State] = set() # Conjunto de estados visitados
    
    def clear(self):
        super().clear()
        
        self.structure: Queue[State] = Queue()
        
        self.closed_set.clear()
    
    def search(self, start, goal):
        self.clear()
        
        self.structure.put(start)
        self.closed_set.add(start)
        
        while not self.structure.empty():
            self.update_memory()
            
            self.current = self.structure.get()
            
            if self.current == goal:
                self.update_path()
                
                break

            self.update_expanded()
            
            for cost, neighbor in self.current.expand():
                if neighbor not in self.closed_set:
                    self.update_branches()
                    
                    self.structure.put(neighbor)
                    self.closed_set.add(neighbor)

        self.update_timer()
        self.update_done()

class IterativeDeepeningSearch(Search):
    ''' Algoritmo de busca em profundidade iterativa '''
    
    def __init__(self):
        super().__init__()
        
        self.depth = 0 # Profundidade máxima do algoritmo
    
    def clear(self):
        super().clear()
        
        self.structure: Stack[tuple[int, State]] = Stack()
        
        self.depth = 0
    
    def update_depth(self):
        ''' Atualiza a profundidade do algoritmo '''
        
        self.depth += 1
    
    def search(self, start, goal):
        self.clear()
        
        should_break = False
        
        while True:
            print(f'DEPTH: {self.depth}')
            
            self.structure.clear()
            self.structure.put((self.depth, start))
            
            while not self.structure.empty():
                self.update_memory()
                
                d_score, self.current = self.structure.get()
                
                if self.current == goal:
                    self.update_path()
                    
                    should_break = True
                    break
                
                if d_score <= 0:
                    continue

                current_path = self.current.path()

                if self.current in current_path[:-1]:
                    continue
                
                self.update_expanded()
                
                for cost, neighbor in self.current.expand():
                    self.update_branches()
                    
                    self.structure.put((d_score - 1, neighbor))
                    
            if should_break:
                break
                    
            self.update_depth()
        
        self.update_timer()
        self.update_done()

class AStarSearch(Search):
    def __init__(self, h: Callable[[State, State], int]):
        super().__init__()
        
        self.h = h
        
        self.g_score: dict[State, int] = {}
        
    def clear(self):
        super().clear()
        
        self.structure: PriorityQueue[tuple[int, int, State]] = PriorityQueue()
        
        self.g_score.clear()

    def prepare(self, start: State):
        ''' Prepara o algoritmo para a execução (Reutilizado no BidirectionalAStarSearch) '''
        
        self.structure.put((0, 0, start))
        self.g_score[start] = 0

    def step(self, goal: State):
        ''' Executa um passo do algoritmo (Reutilizado no BidirectionalAStarSearch) '''

        if self.current is None:
            return

        self.update_expanded()
            
        for cost, neighbor in self.current.expand():
            tentative_g_score = self.g_score[self.current] + cost        
            
            if neighbor not in self.g_score or tentative_g_score < self.g_score[neighbor]:
                self.update_branches()
                
                h_score = self.h(neighbor, goal)
            
                self.structure.put((tentative_g_score + h_score, h_score, neighbor))
                self.g_score[neighbor] = tentative_g_score

    def search(self, start, goal):
        self.clear()
        
        self.prepare(start)
        
        while not self.structure.empty():
            self.update_memory()
            
            _, _, self.current = self.structure.get()
            
            if self.current == goal:
                self.update_path()
                
                break
                
            self.step(goal)
             
        self.update_timer()
        self.update_done()

class BidirectionalAStarSearch(Search):  
    def __init__(self, h: Callable[[State, State], int]):
        super().__init__()
        
        self.forward = AStarSearch(h)
        self.backward = AStarSearch(h)
        
    def clear(self):
        super().clear()
        
        self.forward.clear()
        self.backward.clear()
    
    def search(self, start: State, goal: State):
        self.clear()
        
        self.forward.prepare(start)
        self.backward.prepare(goal)
        
        while not self.forward.structure.empty() or not self.backward.structure.empty():
            self.update_memory(self.forward.structure, self.backward.structure)
            
            self.forward.current = None
            self.backward.current = None
            
            if not self.forward.structure.empty():
                _, _, self.forward.current = self.forward.structure.get()
            
            if not self.backward.structure.empty():
                _, _, self.backward.current = self.backward.structure.get()
                
            if (
                self.forward.current == self.backward.current 
                or self.forward.current in self.backward.g_score or 
                self.backward.current in self.forward.g_score
            ):
                if self.forward.current in self.backward.g_score:
                    for item in self.backward.g_score.keys():
                        if self.forward.current != item:
                            continue
                        
                        self.backward.current = item
                        break
        
                elif self.backward.current in self.forward.g_score:
                    for item in self.forward.g_score.keys():
                        if self.backward.current != item:
                            continue
                        
                        self.forward.current = item
                        break
                    
                self.forward.update_path()
                self.backward.update_path()
                
                self.update_path(self.forward.path[:-1], self.backward.path[::-1])
                
                break

            self.forward.step(goal)
            self.backward.step(start)
        
        self.update_expanded(self.forward.expanded, self.backward.expanded)
        self.update_branches(self.forward.branches, self.backward.branches)
        
        self.update_timer()
        self.update_done()