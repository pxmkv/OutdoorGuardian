from machine import I2C, Pin 
from imu import MPU6050
import ssd1306
import time
# Pins according the schematic https://heltec.org/project/wifi-kit-32/
i2c_imu = I2C(-1, scl=Pin(25), sda=Pin(4))
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
imu = MPU6050(i2c_imu)
# for x in range (100):

#     # print all values
#     print(imu.accel.xyz)
#     print(imu.gyro.xyz)
#     print(imu.temperature)

#     # #print a single value, e.g. x value of acceleration
#     # print(imu.accel.x)
#     time.sleep(1)

while True:
    display.text('accX'+str(imu.accel.x), 0, 0, 1)
    display.text('accY'+str(imu.accel.y), 0, 10, 1)
    display.text('accZ'+str(imu.accel.z), 0, 20, 1)
    display.text('gyroX'+str(imu.gyro.x), 0, 30, 1)
    display.text('gyroY'+str(imu.gyro.y), 0, 40, 1)
    display.text('gyroZ'+str(imu.gyro.z), 0, 50, 1)
    display.show()
    time.sleep(0.5)
    display.fill(0)


