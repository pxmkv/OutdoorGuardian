from QMC5883 import QMC5883L
from machine import Pin
import time 
import math
qmc=QMC5883L(scl=25, sda=4)

def calculate_heading(x, y, declination=0):
    heading = math.atan2(y, x)
    heading_degrees = math.degrees(heading)
    heading_degrees += declination

    # Normalize to 0-360
    if heading_degrees < 0:
        heading_degrees += 360
    elif heading_degrees > 360:
        heading_degrees -= 360

    return heading_degrees


while True:
    x, y, _, _, _ =qmc.read()
    declination = -14  # Example declination value
    heading = calculate_heading(x, y, declination)
    print("Heading:", heading, "degrees")

    time.sleep(0.5)
