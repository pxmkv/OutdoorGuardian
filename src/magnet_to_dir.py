from machine import I2C, Pin 
from QMC5883 import QMC5883L

import time
import math
import os

# i2c = I2C(sda=Pin(21), scl=Pin(22))

compass = QMC5883L(scl=22, sda=23)

def calculate_heading(x, y, declination=-14):
    heading = math.atan2(y, x)
    heading_degrees = math.degrees(heading)
    heading_degrees += declination

    # Normalize to 0-360
    if heading_degrees < 0:
        heading_degrees += 360
    elif heading_degrees > 360:
        heading_degrees -= 360

    return heading_degrees 
    
    


# Perform calibration (ensure the sensor is in a 'neutral' magnetic environment)
compass.calibrate(num_samples=200)
print(compass.offset_x, compass.offset_y, compass.offset_z)

# Now use read_calibrated() for compensated readings
for i in range(100):
    x, y, z = compass.read_calibrated()
    # print('xyz ', x, y, z)
    print(calculate_heading(x, y), " degrees")
    time.sleep(0.5)
    

