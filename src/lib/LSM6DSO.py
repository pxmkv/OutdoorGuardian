from machine import Pin
from machine import I2C
from binascii import hexlify
import time

i2c = I2C(1,scl=Pin(22),sda=Pin(23),freq=400000)


for i in range(len(i2c.scan())):
	print(hex(i2c.scan()[i]))


def WHOAMI(i2caddr):
	whoami = i2c.readfrom_mem(i2caddr,0x0F,1)
	print(hex(int.from_bytes(whoami,"little")))

def Temperature(i2caddr):
	temperature = i2c.readfrom_mem(i2caddr,0x20,2)
	if int.from_bytes(temperature,"little") > 32767:
		temperature = int.from_bytes(temperature,"little")-65536
	else:
		temperature = int.from_bytes(temperature,"little")
	print("%4.2f" % ((temperature)/(256) + 25))

def Zaccel(i2caddr):
	zacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2C,2),"little")
	if zacc > 32767:
		zacc = zacc -65536
	print("%4.2f" % (zacc/16393))

def Xaccel(i2caddr):
	xacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x28,2),"little")
	if xacc > 32767:
		xacc = xacc -65536
	print("%4.2f" % (xacc/16393))

def Yaccel(i2caddr):
	yacc = int.from_bytes(i2c.readfrom_mem(i2caddr,0x2A,2),"little")
	if yacc > 32767:
		yacc = yacc -65536
	print("%4.2f" % (yacc/16393))



buff=[0xA0]
i2c.writeto_mem(i2c.scan()[i],0x10,bytes(buff))
i2c.writeto_mem(i2c.scan()[i],0x11,bytes(buff))
time.sleep(0.1)


try:
	while(1):
		WHOAMI(i2c.scan()[i])
		Temperature(i2c.scan()[i])
		Xaccel(i2c.scan()[i])
		Yaccel(i2c.scan()[i])
		Zaccel(i2c.scan()[i])
		time.sleep(1)

except KeyboardInterrupt:
	i2c.deinit()
	pass
