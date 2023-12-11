# in the implementation the following reference codes were used
#https://github.com/robert-hh/QMC5883/blob/master/qmc5883.py
#https://github.com/gvalkov/micropython-esp8266-hmc5883l/blob/master/hmc5883l.py

import math
import machine
from ustruct import pack
from array import array
import time

class QMC5883L():
    def __init__(self, scl=5, sda=4):
        self.i2c = machine.I2C(scl=machine.Pin(scl), sda=machine.Pin(sda), freq=100000)
        self.address = 0x0D  # Address of QMC5883L

        # Initialize sensor
        self.i2c.start()

        # Set/reset period
        self.i2c.writeto_mem(self.address, 0x0B, b'\x01')

        # Continuous measurement mode, 200Hz, 8 Gauss, OSR = 512
        self.i2c.writeto_mem(self.address, 0x09, b'\x1D')

        self.i2c.stop()

        # Reserve memory for the raw xyz measurements
        self.data = bytearray(6)
        
        self.deg_offset = 180
        
	try:
	    with open('config.dat') as f:
	        line = f.readline().strip()  # Read the first line
		# Assuming the line is in the format "[x, y, z]"
		offsets = line.strip('[]').split(',')  # Remove brackets and split by comma
		self.offset_x = float(offsets[0].strip())
		self.offset_y = float(offsets[1].strip())
		self.offset_z = float(offsets[2].strip())
	    #configs=json.loads(lines[0])
	except OSError: #no config.dat found, will use default config data and save to config.dat
	    configs = [651.53, 375.6, 24.38]
	    with open('config.dat', "w") as f: 
	        f.write(''.join(str(configs)))

        
    def update(self, raw): #update config settings 

        configs = raw# Load the string as JSON and convert it to a list
        with open('config.dat', "w") as f:
            f.write(''.join(str(configs)))

        
    def calculate_heading(self, declination=-14):
        x, y, _ = self.read_calibrated()
        heading_degrees = math.degrees(math.atan2(y, x) )
        heading_degrees += declination
        heading_degrees += self.deg_offset
        

	    # Normalize to 0-360
        if heading_degrees < 0:
    	    heading_degrees += 360
        elif heading_degrees > 360:
       	    heading_degrees -= 360

        return heading_degrees 
    
    def calibrate(self, num_samples=100):
        sum_x, sum_y, sum_z = 0, 0, 0

        for _ in range(num_samples):
            x, y, z = self.read()
            sum_x += x
            sum_y += y
            sum_z += z
            time.sleep(0.1)

        self.offset_x = sum_x / num_samples
        self.offset_y = sum_y / num_samples
        self.offset_z = sum_z / num_samples
        
        offsets = [self.offset_x, self.offset_y, self.offset_z]
        print(offsets)
        
        self.update(offsets)
        

    

    def read_calibrated(self):
        x, y, z = self.read()
        return (x - self.offset_x, y - self.offset_y, z - self.offset_z)

    def read(self):
        # Read data register 00H ~ 05H
        self.i2c.readfrom_mem_into(self.address, 0x00, self.data)
        time.sleep(0.005)

        x = (self.data[1] << 8) | self.data[0]
        y = (self.data[3] << 8) | self.data[2]
        z = (self.data[5] << 8) | self.data[4]

        # Convert to signed integers
        x = x if x < 32768 else x - 65536
        y = y if y < 32768 else y - 65536
        z = z if z < 32768 else z - 65536

        # Adjust scale and offset as necessary
        scale = 1  # Adjust as per your calibration
        temperature_offset = 50.0  # Adjust as per your calibration

        return (x / scale, y / scale, z / scale)

