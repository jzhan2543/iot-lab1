import picar_4wd as fc
import numpy as np
from math import sin, cos, radians

#changing print settings to display the large array
import sys
np.set_printoptions(suppress=True,linewidth=sys.maxsize,threshold=sys.maxsize)


def scan_and_map():
    #declaring variables
    STEP = 18
    ANGLE_RANGE = 180
    max_angle = ANGLE_RANGE/2
    min_angle = -ANGLE_RANGE/2
    us_step = STEP
    supersonic_data = []
    current_angle = 0

    #scanning 180 degrees and returning (angle,distance) tuples as a list called supersonic_data
    for step in range(int((2*ANGLE_RANGE / STEP))):
        supersonic_data.append((current_angle,fc.get_distance_at(current_angle)))
        current_angle += us_step
        if current_angle >= max_angle:
            current_angle = max_angle
            us_step = -STEP
        elif current_angle <= min_angle:
            current_angle = min_angle
            us_step = STEP
    return supersonic_data


def get_coords(car_position,angle,distance):
    #converts angle + distance tuples into a numpy array position around our car, which is located at the bottom center
    #where the angle is measured with -90 degrees meaning the left of the car and 90 degrees meaning the right
    x = distance * cos(radians(90-angle))
    y = distance * sin(radians(90-angle))
    return car_position[0]-round(y), car_position[1]+round(x)

def place_objects(supersonic_data,gridsize=(100,101)):
    #supersonic_data is a list of tuples in the form (angle, distance)
    #gridsize is a tuple np.arry shape (#rows,#columns) that builds the grid
    #the cars position is marked an 8 at the bottom center

    #creating grid and car location
    grid = np.zeros(gridsize, dtype=np.int32)
    car_position = (-1,int(grid.shape[1]/2))
    grid[car_position] = 8

    #writing '1's to the grid to display objects
    for datum in supersonic_data:
        grid[get_coords(car_position,*datum)] = 1
    return grid

if __name__ == "__main__":
    supersonic_data = scan_and_map()
    print(place_objects(supersonic_data))
