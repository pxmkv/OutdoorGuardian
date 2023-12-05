from time import sleep
import ssd1306
from machine import Pin, I2C, SPI
from sx127x import SX127x
from config import *

device_spi = SPI(baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(5, Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(27, Pin.OUT, Pin.PULL_UP),
        miso = Pin(19, Pin.IN, Pin.PULL_UP))

lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)
print("LoRa Receiver")
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)



while True:
    print("Checking for packet...")
    if lora.received_packet():
        print("Packet received")
        
        try:
            payload = lora.read_payload()
            print("Received payload:", payload)
        except Exception as e:
            print("Error reading payload:", e)
    else:
        print("No packet received")
        lora.blink_led()
    sleep(1)  # Adjust sleep time as needed