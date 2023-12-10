# Import necessary modules
from machine import Pin, SPI
from lora import LoRa  # Assuming lora is a module or class you have for LoRa communication
import time

# Configuration parameters (can be moved to config.py)
FREQUENCY = 915.0
BANDWIDTH = 250000
SPREADING_FACTOR = 10
CODING_RATE = 5
CS_PIN = 18
RX_PIN = 26
SCK_PIN = 5
MOSI_PIN = 27
MISO_PIN = 19

# Global LoRa instance
lora = None

def setup_lora():
    global lora
    # SPI setup
    spi = SPI(
        1,
        baudrate=10000000,
        sck=Pin(SCK_PIN, Pin.OUT, Pin.PULL_DOWN),
        mosi=Pin(MOSI_PIN, Pin.OUT, Pin.PULL_UP),
        miso=Pin(MISO_PIN, Pin.IN, Pin.PULL_UP),
    )
    spi.init()

    # LoRa setup
    lora = LoRa(
        spi,
        cs=Pin(CS_PIN, Pin.OUT),
        rx=Pin(RX_PIN, Pin.IN),
        frequency=FREQUENCY,
        bandwidth=BANDWIDTH,
        spreading_factor=SPREADING_FACTOR,
        coding_rate=CODING_RATE,
    )
    lora.on_recv(callback)
    lora.recv()  # Put LoRa in receive mode

def send_message(message):
    if lora:
        lora.send(message)
    else:
        print("LoRa not initialized")

def callback(packet):
    # Handle received packet
    print("Received LoRa packet:", packet)
    # You can add more complex processing here

def get_last_received_packet():
    # If you want to store and retrieve the last received packet
    pass  # Implement this as per your requirement

