#import needed python modules
import picar_4wd as fc
import random
import time

#set default speed
speed = 30

#define backwards turn
def turn_backwards(speed):
  fc.turn_right(speed)
  fc.turn_right(speed)
  
def main():
    while True:
        #scan_step using default value of 35 cm distance
        #scan_list is an array of 11 status readings (at 18 degree increments each) with values of 2 (greater than ref distance), 1 (if between 10 and ref), or 0 (if lower than ref)
        scan_list = fc.scan_step(35)
        #check if array is empty
        if not scan_list:
            continue
        #slicing values from position 3 to 7
        tmp = scan_list[3:7]
        print(tmp)
        #if at or less than ref distance then trigger condition to stop, go backwards, sleep, and pick a random direction to move in
        if tmp != [2,2,2,2]:
            fc.stop()
            fc.backward(speed)
            time.sleep(0.5)
            list_of_directions = [fc.turn_right, fc.turn_left, turn_backwards]
            random.choice(list_of_directions)(speed)
        #else keep moving forward
        else:
            fc.forward(speed)

if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()
