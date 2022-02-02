import numpy as np 
import math

ACTIONS = ['left', 'up', 'right', 'down']

class Node: 
    def __init__(self): 
        self.position = (0,0)
        self.parent = None #dunno if i need this 
        
        self.g = 0 #exact cost of path from starting node to any node 
        self.h = 0 #heuristic estimated cost from node n to goal node 
        self.f = 0 #lowest cost in neighborhood node n 


def shortest_dist(a, b): 
    x1, y1 = a
    x2, y2 = b 
    return math.abs(x1 - x2) + math.abs(y1 - y2)

def calculate_best_route(map, loc, goal, heuristic='greedy'): 
    """
    Based on A* 

    :map      : 2d numpy array 
    :loc      : location of current car
    :goal     : location of potential goal
    :heuristic: default shortest path 
    
    Returns best action and best path available
    """
    open = []
    closed = [] 
    open.append(loc)

    if heuristic is 'greedy': 
      while open:
        #f(n) 
        min_cost = np.argmin([n.f for n in open])
        current = open[min_cost]
        closed.append(open.pop(min_cost))


        # n.position 
        # y2, y1 = goal.position

    return 

if __name__ == "__main__": 
    #set up 
    path = calculate_best_route()

