from machine import UART, Pin
import micropyGPS
import time
from machine import I2S,Pin,SDCard,I2C,SPI,UART
import ssd1306

# Initialize GPS
uart = UART(1, baudrate=9600, tx=14, rx=34)  # Update pins according to your hardware setup
my_gps = micropyGPS.MicropyGPS()
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    if uart.any():
        my_sentence = uart.readline().decode('utf-8')
        for x in my_sentence:
            my_gps.update(x)

        # Check if the data is valid
        if my_gps.valid:
            print("valid! yay!!")
            print('Latitude:', str(my_gps.latitude))
            print('Longitude:', str(my_gps.longitude))

            display.text(str(my_gps.latitude), 0, 0, 1)
            display.text(str(my_gps.longitude), 0, 10, 1)
            display.show()
            display.fill(0)
            # print('Satellites in View:', my_gps.satellites_in_view)
            # print('Satellites in Use:', my_gps.satellites_in_use)
            # print('Time Since Last Fix:', my_gps.time_since_fix())
        else:
            print("Waiting for GPS fix...")
            print("Raw GPS data:", my_sentence)
            display.text('RAW', 0, 0, 1)
            display.text(my_sentence, 0, 10, 1)
            display.show()
            display.fill(0)
        # Optional: Log GPS data
        # my_gps.start_logging('gps_log.txt')
        # my_gps.write_log(my_sentence)
        # my_gps.stop_logging()

    else:
        print("No data from GPS module.")

    time.sleep(1)  # Adjust the sleep time as needed

