
import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

with open('2.wav', 'wb') as file:
    while True:
        host, msg = e.recv()
        if msg:
            # Check for the end of the file transmission
            if msg == b'end':
                break
            # Write the received chunk to the file
            file.write(msg)