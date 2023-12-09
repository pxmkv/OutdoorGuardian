import os
import time
import urandom
import uasyncio as asyncio
from machine import I2S,Pin,SDCard,I2C
import ssd1306
import _thread
import network
import espnow

#config
sd = SDCard(slot=3)  # sck=18, mosi=23, miso=19, cs=5
os.mount(sd, "/sd")
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


btn   = Pin(35,Pin.IN,Pin.PULL_UP)


# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)

e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()




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


def callback(data):
    return

lora.on_recv(callback)
