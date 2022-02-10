import picar_4wd as fc
import numpy as np
from numpymap import supersonic_scan, cartesian_distance, dda_line, place_objects
from math import sin, cos, radians, sqrt
import astar_nav
import detect
import detect.tflite
import coco_labels.txt
import time

class car:
    def __init__(self, position = (49,25), direction = 0, speed = 30):
        self.position = position
        self.direction = direction
        self.speed = speed
    
    def get_direction(self):
        return self.direction
    
    def get_position(self):
        return self.position

    def move_forward(self, x=1):
        #Moves the car 5cm times x and updates location
        fc.forward(self.speed)
        time.sleep(.15*x)
        fc.stop
        position_delta = (sin(radians(90-self.direction)), cos(radians(90-self.direction)))
        self.position = (self.position[0]+position_delta[0], self.position[1] + position_delta[1])
        return 

    def turn_left(self):
        #rotates car 90 degrees left and updates direction
        fc.turn_left(self.speed)
        time.sleep(1.1)
        fc.stop
        self.direction -= 90 
        return 

    def turn_right(self):
        #rotates car 90 degrees right and updates direction
        fc.turn_right(self.speed)
        time.sleep(.85)
        fc.stop
        self.direction += 90 
        return 

    def naive_maneuver(self,target_coordinates):
        moves = 0
        for coord in target_coordinates:
            if moves > 10:
                return
            moves += 1
            next_move = (self.position[0]-coord[0], coord[1] - self.position[1])
            if next_move[0] == -1:
                if self.direction == 0:
                    self.move_forward()
                elif self.direction == 90:
                    self.turn_left()
                    self.move_forward()
                elif self.direction == -90:
                    self.turn_right()
                    self.move_forward()
                self.position = (self.position[0]-1, self.position[1])
            elif next_move[1] == 1:
                if self.direction == 90:
                    self.move_forward()
                elif self.direction == 0:
                    self.turn_right()
                    self.move_forward()
                elif self.direction == -90:
                    raise Exception('facing left moving right')
                self.position = (self.position[0],self.position[1]+1)
            elif next_move[1] == -1:
                if self.direction == -90:
                    self.move_forward()
                elif self.direction == 0:
                    self.turn_left()
                    self.move_forward()
                elif self.direction == 90:
                    raise Exception('facing right moving left')
                self.position = (self.position[0], self.position[1]-1)
            else:
                raise Exception('weird next move: ', next_move)
        return

if __name__ == "__main__":
    try:
        #create 50x51 numpy array
        master_map = np.zeros((50,51), dtype=np.int32)
        #start at bottom center
        starting_position = (master_map.shape[0]-1,int(master_map.shape[1]/2))


#        define end goal
#        x = input("Enter x goal :")
#        y = input("Enter y goal :")
#        end_goal = (int(x),int(y)) #TBD
        end_goal = (0,0) #tbd
        wall_e = car() 

        print("starting position: " + str(starting_position))
        print("goal" + str(end_goal))
        print(master_map.tolist())

        while wall_e.get_position() != end_goal:
            #Scan with camera for stop signs:
                #if stop sign, stop for 5 seconds and dont scan again
            supersonic_data = supersonic_scan()
            master_map = place_objects(supersonic_data,wall_e.get_position(),wall_e.get_direction(),master_map)
            next_steps = astar_nav.calculate_best_route(master_map,wall_e.get_position(),end_goal)
            wall_e.naive_maneuver(next_steps)

    finally: 
        print('car position: ', wall_e.get_position())
        fc.stop()
