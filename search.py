from typing import Callable
from queue import PriorityQueue, Queue, LifoQueue
from time import time

from game import NPuzzleState

class Search:
    def __init__(self):
        self.timer = 0
        
        self.memory = 0
        self.expanded = 0
        self.cycles = 0
        
        self.path: list[NPuzzleState] = []

    def clear(self):
        self.timer = time()
        
        self.memory = 0
        self.expanded = 0
        self.cycles = 0
        
        self.path.clear()
        
    def update_timer(self):
        self.timer = time() - self.timer

    def update_memory(self, *queue: Queue):
        self.memory = max(self.memory, sum(q.qsize() for q in queue))

    def update_expanded(self):
        self.expanded += 1

    def update_cycles(self):
        self.cycles += 1
        
    def update_path(self, *paths: list[NPuzzleState]):
        for path in paths:
            self.path.extend(path)

    def search(self, start: NPuzzleState, goal: NPuzzleState):
        raise NotImplementedError()

class BreadthFirstSearch(Search):
    def search(self, start, goal):
        self.clear()
        
        queue: Queue[NPuzzleState] = Queue()
        queue.put(start)
        
        closed_set: set[NPuzzleState] = set()
        
        while not queue.empty():
            self.update_memory(queue)
            
            current = queue.get()
            closed_set.add(current)
            
            if current == goal:
                break

            self.update_cycles()

            for neighbor in current.expand():
                if neighbor not in closed_set:
                    self.update_expanded()
                    
                    queue.put(neighbor)
              
        self.update_path(current.path())
        
        self.update_timer()

class IterativeDeepeningSearch(Search):
    def search(self, start, goal):
        self.clear()
        
        depth = 0
        
        while True:
            print(f'DEPTH: {depth}')
            
            stack: LifoQueue[tuple[int, NPuzzleState]] = LifoQueue()
            stack.put((depth, start))
            
            should_break = False
            
            while not stack.empty():
                self.update_memory(stack)
                
                d_score, current = stack.get()
                
                if current == goal:
                    should_break = True
                    break
                
                if d_score <= 0:
                    continue

                current_path = current.path()

                if current in current_path[:-1]:
                    continue
                
                self.update_cycles()
                
                for neighbor in current.expand():
                    self.update_expanded()
                    
                    stack.put((d_score - 1, neighbor))
                    
            if should_break:
                break
                    
            depth += 1

        self.update_path(current.path())
        
        self.update_timer()

class AStarSearch(Search):
    def __init__(self, h: Callable[[NPuzzleState, NPuzzleState], int]):
        super().__init__()
        
        self.h = h
    
    def search(self, start, goal):
        self.clear()
        
        priority_queue: PriorityQueue[tuple[int, int, NPuzzleState]] = PriorityQueue()
        priority_queue.put((0, 0, start))
        
        g_score = { start: 0 }
        
        while not priority_queue.empty():
            self.update_memory(priority_queue)
            
            _, _, current = priority_queue.get()
            
            if current == goal:
                break
        
            tentative_g_score = g_score[current] + 1        
            
            self.update_cycles()
            
            for neighbor in current.expand():
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    self.update_expanded()
                
                    h_score = self.h(neighbor, goal)
                
                    priority_queue.put((tentative_g_score + h_score, h_score, neighbor))
                    
                    g_score[neighbor] = tentative_g_score
             
        self.update_path(current.path())
        
        self.update_timer()

class BidirectionalAStarSearch(Search):  
    def __init__(self, h: Callable[[NPuzzleState, NPuzzleState], int]):
        super().__init__()
        
        self.h = h
    
    def search(self, start: NPuzzleState, goal: NPuzzleState):
        self.clear()
        
        start_priority_queue: PriorityQueue[tuple[int, int, NPuzzleState]] = PriorityQueue()
        start_priority_queue.put((0, 0, start))
        
        goal_priority_queue: PriorityQueue[tuple[int, int, NPuzzleState]] = PriorityQueue()
        goal_priority_queue.put((0, 0, goal))
        
        start_closed_set: set[NPuzzleState] = set()
        goal_closed_set: set[NPuzzleState] = set()
        
        start_g_score = { start: 0 }
        goal_g_score = { goal: 0 }
        
        while not start_priority_queue.empty() and not goal_priority_queue.empty():
            self.update_memory(start_priority_queue, goal_priority_queue)
            
            _, _, start_current = start_priority_queue.get()
            start_closed_set.add(start_current)
            
            _, _, goal_current = goal_priority_queue.get()
            goal_closed_set.add(goal_current)
        
            if start_current == goal_current:
                break
            
            if start_current in goal_closed_set:
                for goal_closed_item in goal_closed_set:
                    if start_current == goal_closed_item:
                        goal_current = goal_closed_item
                        break
                    
                break

            if goal_current in start_closed_set:
                for start_closed_item in start_closed_set:
                    if goal_current == start_closed_item:
                        start_current = start_closed_item
                        break
                    
                break

            for current in [start_current, goal_current]:
                if current == start_current:
                    g_score = start_g_score
                    priority_queue = start_priority_queue
                    target = goal
                else:  
                    g_score = goal_g_score
                    priority_queue = goal_priority_queue
                    target = start
                
                tentative_g_score = g_score[current] + 1
                
                self.update_cycles()
                
                for neighbor in current.expand():
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        
                        self.update_expanded()
                    
                        h_score = self.h(neighbor, target)
                    
                        priority_queue.put((tentative_g_score + h_score, h_score, neighbor))
                        
                        g_score[neighbor] = tentative_g_score

        start_path = start_current.path()
        goal_path = goal_current.path()
        
        self.update_path(start_path[:-1], goal_path[::-1])

        self.update_timer()
        