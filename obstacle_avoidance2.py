import picar_4wd as fc
import random

speed = 30

def turn_backwards(speed):
  fc.turn_right(speed)
  fc.turn_right(speed)
  
def main():
    while True:
        scan_list = fc.scan_step(35)
        
        if not scan_list:
            continue
            
        tmp = scan_list[3:7]
        print(tmp)
        
        if tmp != [2,2,2,2]:
            fc.stop()
            fc.backward(speed)
            list_of_directions = [fc.turn_right, fc.turn_left, turn_backwards]
            random.choice(list_of_directions)(speed)
        else:
            fc.forward(speed)

if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()

main()
