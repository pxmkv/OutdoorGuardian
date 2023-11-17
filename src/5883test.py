from QMC5883 import QMC5883L
from machine import Pin
import time 
qmc=QMC5883L(scl=22, sda=23)

while True:
    x, y, z, status, temp =qmc.read()
    print (x, y, z, status, temp)
    time.sleep(0.5)
