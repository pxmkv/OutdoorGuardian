from machine import I2C, Pin 
from QMC5883 import QMC5883L
import ssd1306
import time
import math

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

minx = 32767
maxx = -32768
miny = 32767
maxy = -32768

for i in range(50):
    x, y, _, _, _ = compass.read()
    declination = 10
    heading = calculate_heading(x, y, declination)
    print("Heading:", heading, "degrees")

    # Calculate min and max values
    if x < minx:
        minx = x
    if x > maxx:
        maxx = x
    if y < miny:
        miny = y
    if y > maxy:
        maxy = y

    time.sleep(0.1)

# Calculate offsets
x_offset = (maxx + minx) // 2
y_offset = (maxy + miny) // 2

print("minx:", minx)
print("miny:", miny)
print("maxx:", maxx)
print("maxy:", maxy)
print("x offset:", x_offset)
print("y offset:", y_offset)
