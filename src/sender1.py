from machine import Pin, SPI
import time
import LoRa

# Initialize the LoRa module
spi = SPI(2, baudrate=10000000, polarity=0, phase=0)
nss = Pin(18, Pin.OUT)
reset = Pin(14, Pin.OUT)

# Create the LoRaWAN instance
lora = LoRa(spi, nss, reset)

# Start the LoRa module
lora.begin(915E6)  # Set frequency to 915 MHz

while True:
    lora.send_packet("Hello, LoRa!")
    print("Message sent")
    time.sleep(5)

