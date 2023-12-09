from time import sleep
from config import *
import ssd1306
from machine import Pin, I2C, SPI
from sx127x import SX127x
from config import *
def send(string):
        device_spi = SPI(baudrate = 10000000, 
                polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
                sck = Pin(5, Pin.OUT, Pin.PULL_DOWN),
                mosi = Pin(27, Pin.OUT, Pin.PULL_UP),
                miso = Pin(19, Pin.IN, Pin.PULL_UP))
                
        lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)
        counter = 0
        print("LoRa Sender")
        i2c = I2C(sda=Pin(21), scl=Pin(22))
        display = ssd1306.SSD1306_I2C(128, 64, i2c)

        while True:
                payload = string.format(counter)
                display.fill(0)  # Clear the display
                display.text("{0} sent text {1}".format(payload, lora.packet_rssi()), 0, 0, 1)
                display.show()
                lora.println(payload)

                counter += 1
                sleep(5)
                
