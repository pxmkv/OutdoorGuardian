import machine
import time
from mpu9250_new import MPU9250
from machine import I2C, Pin
from board import SDA, SCL

MPU9250._chip_id = 115
# 115, 113, 104
i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=400000)
imu = MPU9250(i2c)

t_ms = [];
a_x = [];
# a_y = [];
# a_z = [];

for k in range(100):
    t_ms.append(time.ticks_ms())
    a_x.append(imu.accel.x)
    # a_y.append(imu.accel.y)
    # a_z.append(imu.accel.z)

for k in range(100):
    # data = "{},{},{},{}".format(t_ms[k],a_x[k],a_y[k],a_z[k])
    data = "{},{}".format(t_ms[k],a_x[k])
    print(data)
