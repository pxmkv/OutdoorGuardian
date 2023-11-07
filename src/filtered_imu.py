from machine import I2C, Pin 
from imu import MPU6050
from kalmanfilter import KalmanFilter
import ssd1306
import time
import math
# Pins according the schematic https://heltec.org/project/wifi-kit-32/
i2c_imu = I2C(-1, scl=Pin(25), sda=Pin(4))
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
imu = MPU6050(i2c_imu)

# Example of using the KalmanFilter class with MPU6050 data
# Assuming `mpu` is an object of a class handling the MPU6050 sensor communication

kf = KalmanFilter()
dt = 0.01  # Time step

while True:
    # acc_data = mpu.get_accel_data()  # Get accelerometer data
    # gyro_data = mpu.get_gyro_data()  # Get gyro data

    # Assume that we are only interested in the X-axis angle
    ax = imu.accel.x
    ay = imu.accel.y
    az = imu.accel.z
    
    acc_angle = 180 * math.atan(ax/math.sqrt(ay**2+az**2)) / 3.142 # Calculate angle based on acc_data
    gyro_rate = imu.gyro.x  # Gyroscope rate from gyro data
    
    angle = kf.update(acc_angle, gyro_rate, dt)
    
    time.sleep(dt)
    
    display.text('X'+str(acc_angle), 0, 0, 1)
    # display.text('filteredX'+str(angle), 0, 10, 1)
    # display.text('increment by'+str(gyro_rate * dt), 0, 20, 1)
    

    display.show()
    time.sleep(0.5)
    display.fill(0)
    
    
