import os
import network
import espnow
from machine import I2S,Pin,SDCard,I2C
sd = SDCard(slot=3)  # sck=18, mosi=23, miso=19, cs=5
os.mount(sd, "/sd")

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

with open("/sd/{}".format('2.wav'), 'wb') as file:
    while True:
        host, msg = e.recv()
        if msg:
            # Check for the end of the file transmission
            if msg == b'end':
                break
            # Write the received chunk to the file
            file.write(msg)