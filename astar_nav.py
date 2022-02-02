import numpy as np 
import math

"""
Calculate the Best Route 
Inspired by https://www.redblobgames.com/pathfinding/a-star/implementation.html
"""

ACTIONS = ['left', 'up', 'right', 'down']
POSITIONS = [(0, 1), (0, -1), (1, 0), (0, 1),
             (-1, -1), (-1, 1), (1, -1), (1, 1)]

class Node(): 
    def __init__(self, parent=None, position=None): 
        self.position = position
        self.parent = parent #dunno if i need this 
        
        self.g = 0 #exact cost of path from starting node to any node 
        self.h = 0 #heuristic estimated cost from node n to goal node 
        self.f = 0 #lowest cost in neighborhood node n 

    def __eq__(self, node): 
        return self.position == node.position


def calculate_best_route(map, loc, goal, heuristic='astar'): 
    """
    Based on A* but can be applied to alternate search methods 

    :map      : 2d numpy array 
    :loc      : location of current car
    :goal     : location of potential goal
    :heuristic: default is a* 
    
    Returns list of tuples as best path 
    """

    start_node = Node(None, loc)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, goal)
    end_node.g = end_node.h = end_node.f = 0

    open = []
    closed = [] 
    open.append(start_node)

    if heuristic == 'astar':
        while len(open) > 0:
            #current node 
            current_node = open[0]
            current_index = 0

            for index, node in enumerate(open): 
                # if we find a better low cost node in list we need to check 
                if node.f < current_node.f: 
                    current_node = node 
                    current_index = index      
            
            # remove current node from open list and add to closed list
            open.pop(current_index)
            closed.append(current_node)

            # if we find goal state
            if current_node == end_node: #TODO update __eq__ for this 
                path = [] 
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] #return reversed path 

            # if we haven't found goal: generate children 
            # need to verify which adjacent squares are possible to move to (JEFF: i think it's only 4 not 8)
            children = []

            #rewrite this later 
            for new_position in [(0, 1), (0, -1), (1, 0), (0, 1),
                                 (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                node_position = (
                    current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                
                #ensure in boundaries
                if node_position[0] > (len(map) - 1) or node_position[0] < 0 or node_position[1] > (len(map[len(map)-1]) - 1) or node_position[1] < 0:
                    continue 

                if map[node_position[0]][node_position[1]] != 0:
                    continue

                new_node = Node(parent=current_node, position=node_position)
                children.append(new_node)

            # loop through children and add to open to consider
            for child in children:

                #if we've already checked a position 
                for closed_node in closed: 
                    if child == closed_node: 
                        continue
                
                #generate node values g h f 
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                for open_node in open:
                    if child == open_node and child.g > open_node.g:
                        continue
                
                #add to open to consider 
                open.append(child)


if __name__ == "__main__": 
    #set up 

    map =  [[0, 0, 0, 0, -10, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -10, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -10, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -10, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -10, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -10, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -10, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -10, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -10, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (8, 8)
    path = calculate_best_route(map, start, end)
    print(path)

