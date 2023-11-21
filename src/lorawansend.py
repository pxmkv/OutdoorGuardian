from time import sleep
import  ssd1306

def send(lora):
    counter = 0
    print("LoRa Sender")
    display = Display()

    while True:
        payload = 'Alert: Danger ({0})'.format(counter)
        display.show_text_wrap("{0} RSSI: {1}".format(payload, lora.packet_rssi()))
        lora.println(payload)

        counter += 1
        sleep(5)
