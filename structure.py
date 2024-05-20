from heapq import heappush, heappop
from collections import deque

from typing import Generic, TypeVar

T = TypeVar('T')

class Structure(Generic[T]):
    ''' Classe abstrata que representa uma estrutura de dados. '''
    
    def size(self) -> int:
        ''' Retorna o tamanho da estrutura.'''
        
        raise NotImplementedError()
    
    def empty(self) -> bool:
        ''' Retorna se a estrutura está vazia. '''
        
        raise NotImplementedError()
    
    def put(self, item: T):
        ''' Adiciona um item na estrutura. '''
        
        raise NotImplementedError()
    
    def get(self) -> T:
        ''' Remove e retorna um item da estrutura. '''
        
        raise NotImplementedError()
    
    def clear(self):
        ''' Limpa a estrutura. '''
        
        raise NotImplementedError()

class PriorityQueue(Structure[T]):
    ''' Classe que representa uma fila de prioridade. '''
    
    def __init__(self):
        self.elements: list[T] = []
    
    def size(self):
        return len(self.elements)
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item: T):
        heappush(self.elements, item)
    
    def get(self):
        return heappop(self.elements)

    def clear(self):
        self.elements.clear()

class Queue(Structure[T]):
    ''' Classe que representa uma fila. '''
    
    def __init__(self):
        self.elements: deque[T] = deque()
    
    def size(self):
        return len(self.elements)
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item: T):
        self.elements.append(item)
    
    def get(self):
        return self.elements.popleft()

    def clear(self):
        self.elements.clear()

class Stack(Structure[T]):
    ''' Classe que representa uma pilha. '''
    
    def __init__(self):
        self.elements: deque[T] = deque()
    
    def size(self):
        return len(self.elements)
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item: T):
        self.elements.append(item)
    
    def get(self):
        return self.elements.pop()
    
    def clear(self):
        self.elements.clear()