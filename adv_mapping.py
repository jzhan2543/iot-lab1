from picar_4wd.servo import Servo
from picar_4wd.pwm import PWM
from picar_4wd.Ultrasonic import Ultrasonic
                     
# create an Servo object from a pin
ser = Servo(PWM("P0"))                            

# create an Ultrasonic object from the given pin  
us = Ultrasonic(Pin('D8'), Pin('D9'))    

           

for i in range(-90, 90, 5):
  # set the servo angle
  ser.set_angle(i)      
  # get the distance
  dis_val = us.get_distance()           
  
