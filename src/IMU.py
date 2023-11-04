from machine import I2C, Pin 
from imu import MPU6050
import time
# Pins according the schematic https://heltec.org/project/wifi-kit-32/
i2c = I2C(-1, scl=Pin(25), sda=Pin(4))

imu = MPU6050(i2c)
for x in range (100):

    # print all values
    print(imu.accel.xyz)
    print(imu.gyro.xyz)
    print(imu.temperature)

    # #print a single value, e.g. x value of acceleration
    # print(imu.accel.x)
    time.sleep(1)