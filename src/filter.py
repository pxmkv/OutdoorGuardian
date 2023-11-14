from machine import Pin, I2C
import utime
import math
from imu import MPU6050
 
def calculate_tilt_angles(accel_data):
    x, y, z = accel_data[0], accel_data[1], accel_data[2]
 
    tilt_x = math.atan2(y, math.sqrt(x * x + z * z)) * 180 / math.pi
    tilt_y = math.atan2(-x, math.sqrt(y * y + z * z)) * 180 / math.pi
    tilt_z = math.atan2(z, math.sqrt(x * x + y * y)) * 180 / math.pi
 
    return tilt_x, tilt_y, tilt_z
 
def complementary_filter(pitch, roll, gyro_data, dt, alpha=0.98):
    pitch += gyro_data[0] * dt
    roll -= gyro_data[1] * dt
 
    pitch = alpha * pitch + (1 - alpha) * math.atan2(gyro_data[1], math.sqrt(gyro_data[0] * gyro_data[0] + gyro_data[2] * gyro_data[2])) * 180 / math.pi
    roll = alpha * roll + (1 - alpha) * math.atan2(-gyro_data[0], math.sqrt(gyro_data[1] * gyro_data[1] + gyro_data[2] * gyro_data[2])) * 180 / math.pi
 
    return pitch, roll

i2c = I2C(0, scl=Pin(25), sda=Pin(4), freq=400000)
mpu = MPU6050(i2c)

pitch = 0
roll = 0
prev_time = utime.ticks_ms()

while True:
    # Retrieve sensor data
    temp = mpu.temperature
    accel_data = mpu.accel.xyz
    gyro_data = mpu.gyro.xyz

    curr_time = utime.ticks_ms()
    dt = (curr_time - prev_time) / 1000

    tilt_x, tilt_y, tilt_z = calculate_tilt_angles(accel_data)
    pitch, roll = complementary_filter(pitch, roll, gyro_data, dt)

    prev_time = curr_time
    
    print(tilt_x, tilt_y, tilt_z)
    
    utime.sleep(1)
