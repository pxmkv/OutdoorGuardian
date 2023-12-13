# Echo any messages received (using custom LoRa parameters).
#
# The pin configuration used here is for the first LoRa module of these boards:
# https://makerfabs.com/esp32-lora-gateway.html

from lora import LoRa
from machine import Pin, SPI
from time import sleep

from machine import Pin, I2C
import ssd1306
import time

# using default address 0x3C
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)



# SPI pins
SCK  = 5
MOSI = 27
MISO = 19
# Chip select
CS   = 18
# Receive IRQ
RX   = 26

# Setup SPI
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
# Receive handler
def handler(x):
    print(x)
    display.text(x, 0, 0, 1)
    display.show()
    display.fill(0)


    # Echo message
    lora.send(x)
    # Put module back in recv mode
    lora.recv()

# Set handler
lora.on_recv(handler)
# Put module in recv mode
lora.recv()

# No need for main loop, code is asynchronous

