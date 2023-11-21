from machine import I2C, Pin 
from QMC5883 import QMC5883L
import ssd1306
import time
import math
import csv  # Include the csv module

i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
compass = QMC5883L(scl=25, sda=4)

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

compass_readings = []  # List to store compass readings

for i in range(500):
    x, y, _, _, _ = compass.read()  # Assuming sensor is an instance of your magnetometer class
    declination = 10  # Example declination value
    heading = calculate_heading(x, y, declination)
    print("Heading:", heading, "degrees")

    # Store the reading in the list
    compass_readings.append({
        "X": x,
        "Y": y,
        "Heading": heading
    })
    time.sleep(0.1)

# Writing to CSV
output_filename = "compass_readings.csv"
with open(output_filename, "w", newline="") as csvfile:
    fieldnames = ['X', 'Y', 'Heading']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for reading in compass_readings:
        writer.writerow(reading)

print(f"Data written to {output_filename}")

