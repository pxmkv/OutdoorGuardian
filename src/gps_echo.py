# Echo any messages received (using custom LoRa parameters).
#
# The pin configuration used here is for the first LoRa module of these boards:
# https://makerfabs.com/esp32-lora-gateway.html


from lora import LoRa
from machine import Pin, SPI, UART
from time import sleep

from machine import Pin, I2C
import ssd1306
import time
import micropyGPS
import json
import math

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



def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0

    # Convert coordinates from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def string_to_array(input_str):
    try:
        # Remove outer brackets
        inner_str = input_str.strip('[]')

        # Split the string into main parts
        parts = inner_str.split('], ')

        # Process first part (nested list)
        nested_list_str = parts[0].strip('[]')
        nested_list = []
        for x in nested_list_str.split(', '):
            if is_float(x):
                nested_list.append(float(x) if '.' in x or 'e' in x.lower() or '-' in x else int(x))
            else:
                raise ValueError(f"Invalid number format: {x}")

        # Process the remaining parts
        float_values = []
        for x in parts[1:]:
            if is_float(x):
                float_values.append(float(x))
            else:
                raise ValueError(f"Invalid number format: {x}")

        # Combine and return the result
        return [nested_list] + float_values

    except Exception as e:
        print(f"Error processing input: {e}")
        return None


# Receive handler
def handler(received_packet):
    # Parse the received packet
    parsed_data = string_to_array(received_packet)
    if parsed_data is not None and len(parsed_data) == 3 and isinstance(parsed_data[1], float) and isinstance(parsed_data[2], float):
        # Received packet is valid and contains GPS data
        received_latitude, received_longitude = parsed_data[1], parsed_data[2]

        # Get current GPS data
        current_latitude, current_longitude = get_current_gps_data()  # Implement this function

        # Print current GPS data
        print(f"Current GPS location: Latitude {current_latitude}, Longitude {current_longitude}")

        # Print received GPS data
        print(f"Received GPS location: Latitude {received_latitude}, Longitude {received_longitude}")

        # Calculate distance using Haversine formula
        distance = haversine(current_latitude, current_longitude, received_latitude, received_longitude)
        print(f"Distance to received location: {distance:.2f} km")
    else:
        print("Invalid packet format received")




# Set handler
lora.on_recv(handler)
# Put module in recv mode
lora.recv()

def main():
    # Initialize GPS (if any initialization is needed)
    gps_data = None

    # Wait for initial GPS fix
    while gps_data is None:
        print("Waiting for GPS fix...")
        gps_data = get_packet()
        time.sleep(5)  # Check every 5 seconds

    print("GPS fix obtained.")

    # Update location every minute
    while True:
        new_data = get_packet()
        if new_data:
            gps_data = new_data
            
            

        # Wait for one minute before the next update
        time.sleep(60)

if __name__ == "__main__":
    main()

