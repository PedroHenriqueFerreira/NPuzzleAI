from typing import Optional
from random import choice
from time import sleep
from json import loads

from threading import Thread
from tkinter import Tk, Canvas

from state import State
from search import *

BG_COLOR = '#333'
    
BOX_SIZE = 800
NODE_SIZE = 2

NODE_COLOR = '#666'

LINE_SIZE = 1
LINE_COLOR = '#444'

NODE_START_COLOR = '#F08'
NODE_GOAL_COLOR = '#0FA'
PATH_COLOR = '#0EF'

FPS = 60
INTERVAL_TIME = 2000

DELAY = 0.1

class Coord(State):
    def __init__(
        self, 
        x: float, 
        y: float, 
        map: Optional['Map'] = None, 
        parent: Optional['Coord'] = None
    ):
        self.x = x
        self.y = y
        
        self.map = map
        self.parent = parent

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Coord({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other: Optional['Coord']):
        if other is None:
            return False
        
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: 'Coord'):
        return not self == other

    def distance(self, other: 'Coord') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def expand(self):
        sleep(DELAY)
        
        if self.map is None:
            return []
        
        states = []
        
        for neighbor in self.map.graph[self]:
            cost = self.distance(neighbor)
            state = Coord(neighbor.x, neighbor.y, self.map, self)
            
            states.append((cost, state))
        
        return states

class Map:
    def __init__(self, filepath: str):
        self.filepath = filepath
        
        self.graph: dict[Coord, list[Coord]] = {}
        
        self.min = Coord(float('inf'), float('inf'))
        self.max = Coord(float('-inf'), float('-inf'))
        
        self.load()
    
    def load(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            data = loads(file.read())
            
        for feature in data['features']:
            geometry_type = feature['geometry']['type']
            geometry_coords = feature['geometry']['coordinates']
            
            properties = feature['properties']

            if geometry_type != 'LineString':
                continue

            if properties.get('highway') not in (
                'motorway', 'motorway_link', 'trunk',
                'trunk_link', 'primary', 'primary_link',

                'secondary', 'secondary_link', 'tertiary',
                'tertiary_link', 'road',

                'living_street', 'pedestrian', 'unclassified',
                'residential',
            ):
                continue

            coords = [Coord(*coord, self) for coord in geometry_coords]

            for prev, curr, next in zip([None] + coords[:-1], coords, coords[1:] + [None]):
                if curr not in self.graph:
                    self.graph[curr] = []

                if prev and prev not in self.graph[curr]:
                    self.graph[curr].append(prev)

                if next and next not in self.graph[curr]:
                    self.graph[curr].append(next)
                    
            for coord in coords:
                if self.min.x > coord.x:
                    self.min.x = coord.x
                    
                if self.min.y > coord.y:
                    self.min.y = coord.y
                    
                if self.max.x < coord.x:
                    self.max.x = coord.x
                    
                if self.max.y < coord.y:
                    self.max.y = coord.y

    def draw(self, solver: Search):
        ovals: dict[Coord, int] = {}
        lines: dict[tuple[Coord, Coord], int] = {}
        
        root = Tk()
        root.title('Map')
        
        canvas = Canvas(
            root, 
            width=BOX_SIZE, 
            height=BOX_SIZE, 
            background=BG_COLOR
        )
        canvas.pack()
        
        for coord in map.graph:
            x = (coord.x - map.min.x) / (map.max.x - map.min.x) * BOX_SIZE
            y = (coord.y - map.min.y) / (map.max.y - map.min.y) * BOX_SIZE
            
            ovals[coord] = canvas.create_oval(
                x - NODE_SIZE / 2, 
                y - NODE_SIZE / 2, 
                x + NODE_SIZE / 2, 
                y + NODE_SIZE / 2, 
                fill=NODE_COLOR,
                width=0
            )
        
            for neighbor in map.graph[coord]:
                nx = (neighbor.x - map.min.x) / (map.max.x - map.min.x) * BOX_SIZE
                ny = (neighbor.y - map.min.y) / (map.max.y - map.min.y) * BOX_SIZE
                
                line = canvas.create_line(
                    x, 
                    y, 
                    nx, 
                    ny, 
                    fill=LINE_COLOR,
                    width=LINE_SIZE
                )
                
                lines[(coord, neighbor)] = line
                lines[(neighbor, coord)] = line
            
            for oval in ovals.values():
                canvas.tag_raise(oval)
        
        canvas.itemconfig(ovals[start], fill=NODE_START_COLOR)
        canvas.tag_raise(ovals[start])
        
        canvas.itemconfig(ovals[goal], fill=NODE_GOAL_COLOR)
        canvas.tag_raise(ovals[goal])
    
        def run():
            if solver.is_done:
                for item in solver.path:
                    canvas.itemconfig(ovals[item], fill=PATH_COLOR)
                    canvas.tag_raise(ovals[item])
                    
                    for neighbor in map.graph[item]:
                        if neighbor not in solver.path:
                            continue
                        
                        canvas.itemconfig(lines[(item, neighbor)], fill=PATH_COLOR)
                        canvas.tag_raise(lines[(item, neighbor)])
                
                return canvas.after(INTERVAL_TIME, root.destroy)

            if isinstance(solver, BidirectionalAStarSearch):
                forward_closed_set = list(solver.forward.g_score.keys())
            elif isinstance(solver, IterativeDeepeningSearch | AStarSearch):
                forward_closed_set = solver.current.path()
            else:
                forward_closed_set = solver.closed_set.copy()
            
            for item in forward_closed_set:
                canvas.itemconfig(ovals[item], fill=NODE_START_COLOR)
                canvas.tag_raise(ovals[item])
                
                for neighbor in map.graph[item]:
                    if neighbor not in forward_closed_set:
                        continue
                    
                    canvas.itemconfig(lines[(item, neighbor)], fill=NODE_START_COLOR)
                    canvas.tag_raise(lines[(item, neighbor)])
            
            if isinstance(solver, BidirectionalAStarSearch):
                backward_closed_set = list(solver.backward.g_score.keys())
                for item in backward_closed_set:
                    canvas.itemconfig(ovals[item], fill=NODE_GOAL_COLOR)
                    canvas.tag_raise(ovals[item])
                    
                    for neighbor in map.graph[item]:
                        if neighbor not in backward_closed_set:
                            continue
                        
                        canvas.itemconfig(lines[(item, neighbor)], fill=NODE_GOAL_COLOR)
                        canvas.tag_raise(lines[(item, neighbor)])
                
            canvas.after(1000 // FPS, run)
            
        canvas.after(INTERVAL_TIME, run)
        root.mainloop() 
    
if __name__ == '__main__':
    map = Map('map.geojson')
    
    solver = BidirectionalAStarSearch(Coord.distance)
    
    start = choice(list(map.graph.keys()))
    goal = choice(list(map.graph.keys()))
    
    t = Thread(target=solver.search, args=(start, goal))
    
    t.start()
    
    map.draw(solver)
    
    t.join()
    