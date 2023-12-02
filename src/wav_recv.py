
import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

output_file = open('2.wav', 'wb')

def recv_cb(data):
    print('Data received')
    # Write the incoming data chunk to the file
    output_file.write(data)

# Callback for when data is received
e.on_recv(recv_cb)