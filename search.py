from typing import Callable, Optional
from queue import PriorityQueue, Queue, LifoQueue
from time import time

from game import NPuzzleState

class Search:
    def __init__(self):
        self.timer = 0
        
        self.memory = 0
        self.expanded = 0
        self.cycles = 0
        self.path: Optional[list[NPuzzleState]] = None

    def clear(self):
        self.timer = time()
        
        self.memory = 0
        self.expanded = 0
        self.cycles = 0
        self.path = None
        
    def update_timer(self):
        self.timer = time() - self.timer

    def update_memory(self, *queue: Queue):
        self.memory = max(self.memory, sum(q.qsize() for q in queue))

    def update_expanded(self):
        self.expanded += 1

    def update_cycles(self):
        self.cycles += 1
        
    def update_path(self, path: list[NPuzzleState]):
        self.path = path

    def search(self, start: NPuzzleState, goal: NPuzzleState):
        raise NotImplementedError()

class BreadthFirstSearch(Search):
    def search(self, start, goal):
        self.clear()
        
        queue: Queue[NPuzzleState] = Queue()
        queue.put(start)
        
        closedSet: set[NPuzzleState] = set()
        
        while not queue.empty():
            self.update_memory(queue)
            
            current = queue.get()
            closedSet.add(current)
            
            if current == goal:
                break

            self.update_cycles()

            for neighbor in current.expand():
                if neighbor not in closedSet:
                    self.update_expanded()
                    
                    queue.put(neighbor)
              
        self.update_path(current.path())
        
        self.update_timer()

class IterativeDeepeningSearch(Search):
    def search(self, start, goal):
        self.clear()
        
        depth = 0
        
        while True:
            # print(f'MAX_DEPTH: {depth}')
            
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
        
        priority_queue: PriorityQueue[tuple[int, NPuzzleState]] = PriorityQueue()
        priority_queue.put((0, start))
        
        g_score = { start: 0 }
        
        while not priority_queue.empty():
            self.update_memory(priority_queue)
            
            f_score, current = priority_queue.get()
        
            if current == goal:
                break
        
            tentative_g_score = g_score[current] + 1        
            
            self.update_cycles()
            
            for neighbor in current.expand():
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    self.update_expanded()
                
                    priority_queue.put((tentative_g_score + self.h(neighbor, goal), neighbor))
                    
                    g_score[neighbor] = tentative_g_score
             
        self.update_path(current.path())
        
        self.update_timer()

class BidirectionalAStarSearch(Search):
    def __init__(self, h: Callable[[NPuzzleState, NPuzzleState], int]):
        super().__init__()
        
        self.h = h
    
    def search(self, start: NPuzzleState, goal: NPuzzleState):
        self.clear()
        
        start_priority_queue: PriorityQueue[tuple[int, NPuzzleState]] = PriorityQueue()
        start_priority_queue.put((0, start))
        
        goal_priority_queue: PriorityQueue[tuple[int, NPuzzleState]] = PriorityQueue()
        goal_priority_queue.put((0, goal))
        
        start_g_score = { start: 0 }
        goal_g_score = { goal: 0 }
        
        start_target = goal
        goal_target = start
        
        while not start_priority_queue.empty() or not goal_priority_queue.empty():
            self.update_memory(start_priority_queue, goal_priority_queue)
            
            start_current = None
            goal_current = None
            
            if not start_priority_queue.empty():
                start_f_score, start_current = start_priority_queue.get()
                
            if not goal_priority_queue.empty(): 
                goal_f_score, goal_current = goal_priority_queue.get()
        
            if start_current == goal_current:
                break

            start_target = goal_current
            goal_target = start_current
            
            for current in [start_current, goal_current]:
                if current is None:
                    continue
                
                if current == start_current:
                    g_score = start_g_score
                    open_list = start_priority_queue
                    target = start_target
                else:  
                    g_score = goal_g_score
                    open_list = goal_priority_queue
                    target = goal_target
                    
                tentative_g_score = g_score[current] + 1
                
                self.update_cycles()
                
                for neighbor in current.expand():
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        self.update_expanded()
                    
                        open_list.put((tentative_g_score + self.h(neighbor, target), neighbor))
                        
                        g_score[neighbor] = tentative_g_score

        start_path = start_current.path()
        goal_path = goal_current.path()
        
        self.update_path(start_path[:-1] + goal_path[::-1])

        self.update_timer()