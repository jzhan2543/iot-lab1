import picar_4wd as fc
import numpy as np
from numpymap import supersonic_scan, cartesian_distance, dda_line, place_objects
from math import sin, cos, radians, sqrt
import astar_nav
# import detect.py
# import detect.tflite
# import coco_labels.txt
import time

class car:
    def __init__(self, position = [49,25], direction = 0, speed = 30):
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
        # position_delta = (sin(radians(90-self.direction)), cos(radians(90-self.direction)))
        # self.position = (self.position[0]+position_delta[0], self.position[1] + position_delta[1])
        return 

    def turn_left(self):
        #rotates car 90 degrees left and updates direction
        fc.turn_left(self.speed)
        time.sleep(0.87) #adjust this 
        fc.stop
        time.sleep(0.1)
        self.direction -= 90 
        return 

    def turn_right(self):
        #rotates car 90 degrees right and updates direction
        fc.turn_right(self.speed)
        time.sleep(0.80)  # adjust this
        fc.stop
        time.sleep(0.1)
        self.direction += 90 
        return 

    def naive_maneuver(self,target_coordinates):
        moves = 0
        x = 1
        len(target_coordinates)-1
        while x <= len(target_coordinates)-1: 
            coord = target_coordinates[x]
            # if moves > 10:
            #     return
            moves += 1
            next_move = (coord[0] - self.position[0], coord[1] - self.position[1])
            
            print()
            print("position: " + str((self.position[0], self.position[1])))
            print("next coord: " + str(coord))
            print("next_move: " + str(next_move)) 

            #"move up 1 row from 2d perspective"
            if next_move[0] == -1:
                print("moving up")
                # if facing up 
                if self.direction == 0:
                    self.move_forward()
                #if facing right
                elif self.direction == 90:
                    self.turn_left()
                    self.move_forward()
                #if facing left 
                elif self.direction == -90:
                    self.turn_right()
                    self.move_forward()
                self.position = [int(self.position[0]-1), int(self.position[1])]
                print("new position: " + str(self.position))

            #"move right 1 col from 2d perspective"
            elif next_move[1] == 1:
                print("moving right")
                #if facing right (2d perspective)
                if self.direction == 90:
                    self.move_forward()
                #if facing up  (2d perspective)
                elif self.direction == 0:
                    self.turn_right()
                    self.move_forward()
                #if facing left (2d perspective)
                elif self.direction == -90:
                    raise Exception('facing left moving right')
                
                self.position = [self.position[0],self.position[1]+1]
                print("new position: " + str(self.position))
            #"move left 1 col from 2d perspective"
            elif next_move[1] == -1:
                #if facing left 
                print("moving left")
                if self.direction == -90:
                    self.move_forward()
                #if facing up 
                elif self.direction == 0:
                    self.turn_left()
                    self.move_forward()
                #if facing right 
                elif self.direction == 90:
                    raise Exception('facing right moving left')
                
                # Jeff: i think already done
                self.position = [self.position[0], self.position[1]-1]
                print("new position: " + str(self.position))
            else:
                raise Exception('weird next move: ', next_move)
            
            x = x + 1
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
        end_goal = (40,28) #tbd
        print("end_goal: " + str(end_goal))
        wall_e = car() 

        # while wall_e.get_position() != end_goal:
            #Scan with camera for stop signs:
            #if stop sign, stop for 5 seconds and dont scan again

        supersonic_data = supersonic_scan()
        print("supersonic: " + str(supersonic_data))
        master_map = place_objects(supersonic_data,wall_e.get_position(),wall_e.get_direction(),master_map)
        print("master_map: " )
        #+ str(master_map.tolist())
        print(np.matrix(master_map.tolist()))

        next_steps = astar_nav.calculate_best_route(master_map,wall_e.get_position(),end_goal)
        
        print(next_steps)
        wall_e.naive_maneuver(next_steps)

    finally: 
        print('car position: ', wall_e.get_position())
        fc.stop()
