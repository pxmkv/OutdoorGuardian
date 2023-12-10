import os
import time
import urandom
import micropyGPS
import json
import uasyncio as asyncio
from machine import I2S,Pin,SDCard,I2C,SPI,UART
import ssd1306
import _thread
import network
import espnow
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
from time import sleep
from lora import LoRa

#config
# sd = SDCard(slot=3)  # sck=18, mosi=23, miso=19, cs=5
# os.mount(sd, "/sd")
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
btn   = Pin(35,Pin.IN,Pin.PULL_UP)


#Heart rate initialization
heart = MAX30102(i2c=i2c)  # An I2C instance is required
heart.setup_sensor()
heart.set_sample_rate(400)
heart.set_fifo_average(8)
heart.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
sleep(0.5)

# Initialize GPS
uart = UART(1, baudrate=9600, tx=14, rx=34)  # Update pins according to your hardware setup
my_gps = micropyGPS.MicropyGPS()


# Wifi initialization
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
CS   = 18
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


def string_to_array(input_str):
    print(input_str)

    try:
        # Remove outer brackets
        inner_str = input_str.strip('[]')

        # Split the string into main parts
        parts = inner_str.split('], ')
        # Process first part (nested list)
        nested_list_str = parts[0].strip('[]')
        nested_list = []
        for x in nested_list_str.split(', '):
            if '.' in x:
                nested_list.append(float(x))
            elif x.isdigit():
                nested_list.append(int(x))
            else:
                raise ValueError(f"Invalid number format: {x}")

        # Process the remaining parts
        float_values = []
        for x in parts[1:]:
            if x.replace('.', '', 1).isdigit():
                float_values.append(float(x))
            else:
                raise ValueError(f"Invalid number format: {x}")

        # Combine and return the result
        return [nested_list] + float_values

    except Exception as e:
        print(f"Error processing input: {e}")
        return None
    
def convert_to_decimal(loc):
    decimal = loc[0] + loc[1] / 60
    if loc[2] in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_packet():
    try:    
        if uart.any():
            my_sentence = uart.readline().decode('utf-8')
            for x in my_sentence:
                my_gps.update(x)
                

            # Check if the data is valid
            if my_gps.valid:
                return str([my_gps.timestamp, convert_to_decimal(my_gps.latitude), convert_to_decimal(my_gps.longitude)])
                
            else:
                sample = [37, 52.51906, 'N']
                
                print("Waiting for GPS fix...")
                return ""
                # print("Raw GPS data:", my_sentence)
                #print(convert_to_decimal(sample))


            # Optional: Log GPS data
            # my_gps.start_logging('gps_log.txt')
            # my_gps.write_log(my_sentence)
            # my_gps.stop_logging()

        else:
            print("No data from GPS module.")
            return ""
    except :
        print('No GPS')



def callback(data):

    return

def e_mode():
    lora.send('location')#

# lora.on_recv(callback)
def main():
    while True:
        heart.check()
        if heart.available():
            # red = heart.pop_red_from_storage()
            ir  = heart.pop_ir_from_storage()
            if ir < 10000 or ir > 20000:
                e_mode()
            
lora.on_recv(callback)


while True:
   print(string_to_array(get_packet()))
   time.sleep(1)  # Adjust the sleep time as needed