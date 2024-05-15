from typing import Callable
from queue import PriorityQueue, Queue, LifoQueue
from time import time

from n_puzzle import NPuzzleState

class Solver:
    @staticmethod
    def breadth_first_search(
        start: NPuzzleState, 
        goal: NPuzzleState
    ): 
        cycles_count = 0
        expand_count = 0
        max_memory = 0
        initial_time = time()
        
        queue: Queue[NPuzzleState] = Queue()
        queue.put(start)
        
        came_from: dict[NPuzzleState, NPuzzleState] = {}
        
        while not queue.empty():
            memory = queue.qsize()
            
            if memory > max_memory:
                max_memory = memory
            
            current = queue.get()
            
            if current == goal:
                path = [current]

                while current != start:
                    current = came_from[current]
                    path.append(current)

                path.reverse()

                elapsed_time = time() - initial_time

                return path, elapsed_time, max_memory, expand_count, expand_count / cycles_count

            cycles_count += 1

            for neighbor in current.expand():
                expand_count += 1
                
                if neighbor not in came_from:
                    queue.put(neighbor)
                    
                    came_from[neighbor] = current
                    
        elapsed_time = time() - initial_time

        return [], elapsed_time, max_memory, expand_count, expand_count / cycles_count
    
    @staticmethod
    def iterative_deepening_search(
        start: NPuzzleState,
        goal: NPuzzleState
    ):
        cycles_count = 0
        expand_count = 0
        max_memory = 0
        initial_time = time()
        
        depth = 0
        
        while True:
            stack: LifoQueue[NPuzzleState] = LifoQueue()
            stack.put(start)
            
            came_from: dict[NPuzzleState, NPuzzleState] = {}
            
            d_score = { start: depth }
            
            while not stack.empty():
                memory = stack.qsize()
            
                if memory > max_memory:
                    max_memory = memory
                
                current = stack.get()
                
                if current == goal:
                    path = [current]

                    while current != start:
                        current = came_from[current]
                        path.append(current)

                    path.reverse()

                    elapsed_time = time() - initial_time

                    return path, elapsed_time, max_memory, expand_count, expand_count / cycles_count
                
                if d_score[current] <= 0:
                    continue
                
                cycles_count += 1
                
                for neighbor in current.expand():
                    expand_count += 1
                    
                    if neighbor not in came_from:
                        stack.put(neighbor)
                    
                        came_from[neighbor] = current
                    
                        d_score[neighbor] = d_score[current] - 1
                    
            depth += 1
    
    @staticmethod
    def a_star_search(
        start: NPuzzleState, 
        goal: NPuzzleState,
        h: Callable[[NPuzzleState, NPuzzleState], int],
    ):
        cycles_count = 0
        expand_count = 0
        max_memory = 0
        initial_time = time()
        
        priority_queue: PriorityQueue[tuple[int, NPuzzleState]] = PriorityQueue()
        priority_queue.put((0, start))
        
        came_from: dict[NPuzzleState, NPuzzleState] = {}
        
        g_score = { start: 0 }
        
        while not priority_queue.empty():
            memory = priority_queue.qsize()
            
            if memory > max_memory:
                max_memory = memory
            
            _, current = priority_queue.get()
        
            if current == goal:
                path = [current]

                while current != start:
                    current = came_from[current]
                    path.append(current)

                path.reverse()

                elapsed_time = time() - initial_time

                return path, elapsed_time, max_memory, expand_count, expand_count / cycles_count
        
            tentative_g_score = g_score[current] + 1        
            
            cycles_count += 1
            
            for neighbor in current.expand():
                expand_count += 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    priority_queue.put((tentative_g_score + h(neighbor, goal), neighbor))
                    
                    came_from[neighbor] = current
                    
                    g_score[neighbor] = tentative_g_score
                    
        elapsed_time = time() - initial_time
                    
        return [], elapsed_time, max_memory, expand_count, expand_count / cycles_count
    
    @staticmethod
    def bidirectional_a_star_search(
        start: NPuzzleState, 
        goal: NPuzzleState,
        h: Callable[[NPuzzleState, NPuzzleState], int]
    ):
        cycles_count = 0
        expand_count = 0
        max_memory = 0
        initial_time = time()
        
        start_priority_queue: PriorityQueue[tuple[int, NPuzzleState]] = PriorityQueue()
        start_priority_queue.put((0, start))
        
        goal_priority_queue: PriorityQueue[tuple[int, NPuzzleState]] = PriorityQueue()
        goal_priority_queue.put((0, goal))
        
        start_came_from: dict[NPuzzleState, NPuzzleState] = {}
        goal_came_from: dict[NPuzzleState, NPuzzleState] = {}
        
        start_g_score = { start: 0 }
        goal_g_score = { goal: 0 }
        
        start_target = goal
        goal_target = start
        
        while not start_priority_queue.empty() or not goal_priority_queue.empty():
            memory = 0
            
            if start_priority_queue.empty():
                start_current = None
            else:
                _, start_current = start_priority_queue.get()
                memory += start_priority_queue.qsize()
                
            if goal_priority_queue.empty():
                goal_current = None
            else:  
                _, goal_current = goal_priority_queue.get()
                memory += goal_priority_queue.qsize()
        
            if memory > max_memory:
                max_memory = memory
        
            if start_current == goal_current:
                path = [start_current]
                
                while start_current != start:
                    start_current = start_came_from[start_current]
                    path.append(start_current)

                path.reverse()
                
                while goal_current != goal:
                    goal_current = goal_came_from[goal_current]
                    path.append(goal_current)

                elapsed_time = time() - initial_time

                return path, elapsed_time, max_memory, expand_count, expand_count / cycles_count

            start_target = goal_current
            goal_target = start_current
            
            for current in [start_current, goal_current]:
                if current is None:
                    continue
                
                if current == start_current:
                    g_score = start_g_score
                    came_from = start_came_from
                    open_list = start_priority_queue
                    target = start_target
                else:  
                    g_score = goal_g_score
                    came_from = goal_came_from
                    open_list = goal_priority_queue
                    target = goal_target
                    
                cycles_count += 1
                    
                for neighbor in current.expand():
                    expand_count += 1
                    
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        open_list.put((tentative_g_score + h(neighbor, target), neighbor))
                        
                        came_from[neighbor] = current
                        
                        g_score[neighbor] = tentative_g_score

        elapsed_time = time() - initial_time

        return [], elapsed_time, max_memory, expand_count, expand_count / cycles_count