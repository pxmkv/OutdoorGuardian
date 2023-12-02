from machine import I2C, Pin 
from QMC5883 import QMC5883L

import time
import math

# i2c = I2C(sda=Pin(21), scl=Pin(22))

compass = QMC5883L(scl=22, sda=23)

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

output_filename = "compass_readings.csv"
header = "X,Y,Z,Heading\n"

with open(output_filename, "w") as file:
    file.write(header)  # Write the header to the CSV file

    for i in range(500):
        x, y, z, _, _ = compass.read()  # Include Z-axis reading
        declination = 10  # Example declination value
        heading = calculate_heading(x, y, declination)
        print("Heading:", heading, "degrees")

        # Write the reading as a line in the CSV file, including Z value
        line = f"{x},{y},{z},{heading}\n"
        file.write(line)

        time.sleep(0.1)

print(f"Data written to {output_filename}")

