from time import sleep
import ssd1306
from machine import Pin, I2C, SPI
from sx127x import SX127x
from config import *

device_spi = SPI(baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)
print("LoRa Receiver")
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
lora.begin(915E6)

while True:
    if lora.received_packet():
        lora.blink_led()
        payload = lora.read_payload()
        print(payload)
