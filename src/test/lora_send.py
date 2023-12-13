# Send "Hello world!" using the default LoRa parameters every second.
#
# The pin configuration used here is for the first LoRa module of these boards:
# https://makerfabs.com/esp32-lora-gateway.html

from lora import LoRa
from machine import Pin, SPI
from time import sleep

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
n=0
while True:
    lora.send(str(n))
    sleep(1)
    n+=1