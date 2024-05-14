from typing import Callable

from n_puzzle import NPuzzleState

from threading import Thread, Lock

class Solver:
    @staticmethod
    def a_star_search(
        start: NPuzzleState, 
        goal: NPuzzleState,
        h: Callable[[NPuzzleState, NPuzzleState], int],
    ):
        openSet = { start }

        cameFrom: dict[NPuzzleState, NPuzzleState] = {}

        gScore = { start: 0 }
        fScore = { start: h(start, goal) }

        while len(openSet) > 0:
            current = min(openSet, key=lambda x: fScore[x])
            openSet.remove(current)

            if current == goal:
                total_path = [current]

                while current in cameFrom:
                    current = cameFrom[current]
                    total_path.append(current)

                return total_path

            for neighbor in current.expand():
                tentative_gScore = gScore[current] + 1

                if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + h(neighbor, goal)

                    openSet.add(neighbor)
    
        return []
    
    @staticmethod
    def breadth_first_search(
        start: NPuzzleState, 
        goal: NPuzzleState
    ): 
        openList = [ start ]
        closedSet = { start }
        
        cameFrom: dict[NPuzzleState, NPuzzleState] = {}
        
        while len(openList) > 0:
            current = openList.pop(0)
            
            if current == goal:
                total_path = [current]

                while current in cameFrom:
                    current = cameFrom[current]
                    total_path.append(current)

                return total_path

            for neighbor in current.expand():
                if neighbor not in closedSet:
                    cameFrom[neighbor] = current
                    
                    closedSet.add(neighbor)
                    
                    if neighbor not in openList:
                        openList.append(neighbor)

        return []
    
    @staticmethod
    def deep_limited_search(
        start: NPuzzleState,
        goal: NPuzzleState,
        depth: int
    ):
        openList = [ start ]
        closedSet = { start }
        
        cameFrom: dict[NPuzzleState, NPuzzleState] = {}
        
        DScore = { start: depth }
        
        while len(openList) > 0:
            current = openList.pop()
            
            if current == goal:
                total_path = [current]

                while current in cameFrom:
                    current = cameFrom[current]
                    total_path.append(current)

                return total_path
            
            if DScore[current] <= 0:
                continue
            
            for neighbor in current.expand():
                if neighbor not in closedSet:
                    cameFrom[neighbor] = current
                    DScore[neighbor] = DScore[current] - 1
                    
                    closedSet.add(neighbor)
                    
                    if neighbor not in openList:
                        openList.append(neighbor)
        
        return []
    
    def iterative_deepening_search(start: NPuzzleState, goal: NPuzzleState):
        depth = 0
        
        while True:
            total_path = Solver.deep_limited_search(start, goal, depth)

            if total_path:
                return total_path
            
            depth += 1
    
    @staticmethod
    def a_star_bidirectional_search(
        start: NPuzzleState, 
        goal: NPuzzleState,
        h: Callable[[NPuzzleState, NPuzzleState], int]
    ):
        startOpenSet = { start }
        goalOpenSet = { goal }
        
        startCameFrom: dict[NPuzzleState, NPuzzleState] = {}
        goalCameFrom: dict[NPuzzleState, NPuzzleState] = {}
        
        startGScore = { start: 0 }
        goalGScore = { goal: 0 }
        
        startFScore = { start: h(start, goal) }
        goalFScore = { goal: h(goal, start) }
        
        startTarget = goal
        goalTarget = start
        
        while len(startOpenSet) > 0 or len(goalOpenSet) > 0:
            startCurrent = min(startOpenSet, key=lambda x: startFScore[x])
            goalCurrent = min(goalOpenSet, key=lambda x: goalFScore[x])
        
            startOpenSet.remove(startCurrent)
            goalOpenSet.remove(goalCurrent)
        
            if startCurrent == goalCurrent:
                start_total_path = [startCurrent]
                
                while startCurrent in startCameFrom:
                    startCurrent = startCameFrom[startCurrent]
                    start_total_path.append(startCurrent)
                    
                goal_total_path = []
                
                while goalCurrent in goalCameFrom:
                    goalCurrent = goalCameFrom[goalCurrent]
                    goal_total_path.insert(0, goalCurrent)
        
                return goal_total_path + start_total_path
        
            startTarget = goalCurrent
            goalTarget = startCurrent
        
            for current in [startCurrent, goalCurrent]:
                if current == startCurrent:
                    gScore = startGScore
                    fScore = startFScore
                    cameFrom = startCameFrom
                    openSet = startOpenSet
                    target = startTarget
                else:  
                    gScore = goalGScore
                    fScore = goalFScore
                    cameFrom = goalCameFrom
                    openSet = goalOpenSet
                    target = goalTarget
                
                for neighbor in current.expand():
                    tentative_gScore = gScore[current] + 1

                    if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                        cameFrom[neighbor] = current
                        gScore[neighbor] = tentative_gScore
                        fScore[neighbor] = tentative_gScore + h(neighbor, target)
                        
                        openSet.add(neighbor)
    
        return []