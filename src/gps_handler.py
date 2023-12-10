import micropyGPS
from machine import UART
import time

# Configuration parameters (can be moved to config.py)
UART_NUM = 1
BAUD_RATE = 9600
TX_PIN = 14
RX_PIN = 34

# Global GPS instance
my_gps = micropyGPS.MicropyGPS()

def setup_gps():
    global my_gps
    uart = UART(UART_NUM, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN)
    my_gps = micropyGPS.MicropyGPS()

def update_gps():
    global my_gps
    if uart.any():
        sentence = uart.readline().decode('utf-8')
        for x in sentence:
            my_gps.update(x)

def get_current_location():
    # Check if the data is valid
    if my_gps.valid:
        latitude = convert_to_decimal(my_gps.latitude)
        longitude = convert_to_decimal(my_gps.longitude)
        return [my_gps.timestamp, latitude, longitude]
    else:
        return None

def convert_to_decimal(coords):
    decimal = coords[0] + coords[1] / 60
    if coords[2] in ['S', 'W']:
        decimal = -decimal
    return decimal

def has_gps_fix():
    return my_gps.valid


