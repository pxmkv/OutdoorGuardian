from machine import I2C, Pin 
from QMC5883 import QMC5883L
import ssd1306
import time
# Pins according the schematic https://heltec.org/project/wifi-kit-32/

i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
compass = QMC5883L(scl=25, sda=4)

# for x in range (100):

#     # print all values
#     print(imu.accel.xyz)
#     print(imu.gyro.xyz)
#     print(imu.temperature)

#     # #print a single value, e.g. x value of acceleration
#     # print(imu.accel.x)
#     time.sleep(1)

while True:
    x, y, z, _, _ = compass.read()
    print((x, y, z))
    display.text(str(compass.read()), 0, 0, 1)
    
    display.show()
    time.sleep(0.5)
    display.fill(0)


