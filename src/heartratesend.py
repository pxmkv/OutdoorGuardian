from lora import LoRa
from machine import Pin, SPI
from time import sleep
import ssd1306

spi = SPI(
    1,
    baudrate=10000000,
    sck=Pin(SCK, Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(MOSI, Pin.OUT, Pin.PULL_UP),
    miso=Pin(MISO, Pin.IN, Pin.PULL_UP),
)
spi.init()

# Setup LoRa
lora = LoRa(
    spi,
    cs=Pin(CS, Pin.OUT),
    rx=Pin(RX, Pin.IN),
    frequency=915.0,
    bandwidth=250000,
    spreading_factor=10,
    coding_rate=5,
)

danger = False
off = False
def heartratecheck(number, lat, lon):
	if(number > 160):
		danger = True
	elif(number < 40):
		danger = True
	elif(off = False & number = 0)
		danger = True
	else:
		danger = False
	if(danger):
		lora.send('I am in danger, please send help. My location is: ' + lat + ',' + lon)
		#press button so that we can send signal for beep
def deviceturnedoff(previous,heartrate):
    if(previous - heartrate > 100):
        off = True
    #function designed to prevent emergency signals being sent off from the finger being taken off
    
