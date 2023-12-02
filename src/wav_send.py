import network
import time
import os
import espnow

from machine import I2S,Pin,SDCard,I2C
sd = SDCard(slot=3)  # sck=18, mosi=23, miso=19, cs=5
os.mount(sd, "/sd")

# Setup WLAN interface for ESP-NOW
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()


# Function to send a file
def send_file(file_path):
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(250)  # ESP-NOW data limit per transmission
            if not data:
                break
            e.send(peer, data)
            #time.sleep(0.01)  # To avoid sending data too quickly
# Send a file
send_file("/sd/{}".format('2.wav'))
e.send(peer, b'end')

def send_wav():
    with open("/sd/{}".format('2.wav'), 'rb') as f:
        while True:
            data = f.read(250)  # ESP-NOW data limit per transmission
            if not data:
                break
            e.send(peer, data)
        e.send(peer, b'end')
