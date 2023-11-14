from machine import Pin, I2C
import utime
import math
from imu import MPU6050
 
def calculate_tilt_angles(accel_data):
    x, y, z = accel_data['x'], accel_data['y'], accel_data['z']
 
    tilt_x = math.atan2(y, math.sqrt(x * x + z * z)) * 180 / math.pi
    tilt_y = math.atan2(-x, math.sqrt(y * y + z * z)) * 180 / math.pi
    tilt_z = math.atan2(z, math.sqrt(x * x + y * y)) * 180 / math.pi
 
    return tilt_x, tilt_y, tilt_z
 
def complementary_filter(pitch, roll, gyro_data, dt, alpha=0.98):
    pitch += gyro_data['x'] * dt
    roll -= gyro_data['y'] * dt
 
    pitch = alpha * pitch + (1 - alpha) * math.atan2(gyro_data['y'], math.sqrt(gyro_data['x'] * gyro_data['x'] + gyro_data['z'] * gyro_data['z'])) * 180 / math.pi
    roll = alpha * roll + (1 - alpha) * math.atan2(-gyro_data['x'], math.sqrt(gyro_data['y'] * gyro_data['y'] + gyro_data['z'] * gyro_data['z'])) * 180 / math.pi
 
    return pitch, roll

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
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

    print("Temperature: {:.2f} °C".format(temp))
    print("Tilt angles: X: {:.2f}, Y: {:.2f}, Z: {:.2f} degrees".format(tilt_x, tilt_y, tilt_z))
    print("Pitch: {:.2f}, Roll: {:.2f} degrees".format(pitch, roll))
    print("Acceleration: X: {:.2f}, Y: {:.2f}, Z: {:.2f} g".format(*accel_data))
    print("Gyroscope: X: {:.2f}, Y: {:.2f}, Z: {:.2f} °/s".format(*gyro_data))
    utime.sleep(1)
