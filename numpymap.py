import picar_4wd as fc
import numpy as np
from math import sin, cos, radians, sqrt

#changing print settings to display large arrays
import sys
np.set_printoptions(suppress=True,linewidth=sys.maxsize,threshold=sys.maxsize)

def scan_and_map():
    '''
    This function moves the supersonic sensor 180 degrees
    and records angle & distance tuples into list supersonic_data.
    '''
    #declaring variables
    STEP = 10
    ANGLE_RANGE = 180
    max_angle = ANGLE_RANGE/2
    min_angle = -ANGLE_RANGE/2
    us_step = STEP
    supersonic_data = []
    current_angle = -90

    #scanning 180 degrees and returning (angle,distance) tuples as a list called supersonic_data
    for step in range(int(current_angle), int(ANGLE_RANGE/2)+STEP, STEP):
        supersonic_data.append((current_angle,fc.get_distance_at(current_angle)))
        current_angle += us_step
        if current_angle >= max_angle:
            current_angle = max_angle
            us_step = -STEP
        elif current_angle <= min_angle:
            current_angle = min_angle
            us_step = STEP
    return supersonic_data

def get_coords(car_position,angle,distance,scale = 5):
    '''
    Converts polar angle + distance tuples into cartesian coords originating at our car,
    which is located at the bottom center where the angle is measured such that
    -90 degrees is directly to the left of the car and 90 degrees is the right.
    scale will change the scale of the numpy map using floor division, defaulting to 5x.
    '''
    x = (distance // scale) * cos(radians(90-angle))
    y = (distance // scale) * sin(radians(90-angle))
    return car_position[0]-round(y), car_position[1]+round(x)

def cartesian_distance(pta, ptb):
    '''
    Returns the distance between two points given two tuples of coordinates.
    '''
    dist = sqrt((ptb[0]-pta[0])**2 + (ptb[1]-pta[1])**2)
    return dist

def dda_line(obj1,obj2,grid,threshold=4):
    '''
    Draws '1's in numpy array if two points meet the minimum distance threshhold 
    using the digital differential analyzer (dda) Line Generation Algorithm from computer graphics. 
    Default threshhold is 4 since the car is roughly 18cm and we are using a 1:5 scale. 
    '''

    #Checks if objects are closer together than the width of the car then draws the appropriate line

    #Creates steps based on whether the two points are further in the X or Y direction
    if 0 < cartesian_distance(obj1,obj2) <= threshold:
        dy = int(obj2[1]-obj1[1])
        dx = int(obj2[0]-obj1[0])
        if 0 < abs(dx) >= abs(dy):
            steps = int(abs(dx))
        elif 0 < abs(dy) > abs(dx):
            steps = int(abs(dy))

        #establishes increments and coordinates for each point and initializes list 'coordinates' 
        xinc = dx/steps
        yinc = dy/steps
        x = obj1[0]
        y = obj1[1]
        coordinates = []
        i = 0

        #appends coordinates to list and adds them to the grid
        while i < steps:
            i += 1
            x = x + xinc
            y = y + yinc
            coordinates.append((x,y))
        for coord in coordinates:
            grid[int(coord[0]),int(coord[1])] = 1
    return grid

def place_objects(supersonic_data, gridsize=(50,51)):
    '''
    Supersonic_data is a list of polar coordinate tuples in the form (angle, distance).
    Builds a 100x101 array with each vertex representing a 5cm distance.
    Objects detected in supersonice_data are recorded onto the grid with a '1'. 
    the car's position is marked at the bottom center with '8'.
    '''

    #Alternative method to create grid based on furthest object detected and car location:
    #furthest = int(max(supersonic_data, key=lambda x:x[1])[1])
    #gridsize = (furthest, furthest+1)
    
    #Creating grid with car located at bottom center
    grid = np.zeros(gridsize, dtype=np.int32)
    car_position = (-1,int(grid.shape[1]/2))
    grid[car_position] = 8  

    #writing '1's to the grid for recognized data and recording those points in [gridcoords]
    gridcoords = []
    for datum in supersonic_data:
        gridcoords.append(get_coords(car_position,*datum))
        grid[get_coords(car_position,*datum)] = 1
    
    #using gridcoords to draw lines between close objects on the grid
    for i in range(1,len(gridcoords)):
        dda_line(gridcoords[i-1],gridcoords[i],grid)
    
    return grid

if __name__ == "__main__":
    supersonic_data = scan_and_map()
    print(place_objects(supersonic_data))
