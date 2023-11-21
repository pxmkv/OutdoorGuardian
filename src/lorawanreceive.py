import ssd1306

def receive(lora):
    print("LoRa Receiver")
    display = Display()

    while True:
        if lora.received_packet():
            lora.blink_led()
            print('danger')
            payload = lora.read_payload()
            print(payload)
