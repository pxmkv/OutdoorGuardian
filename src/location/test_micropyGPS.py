from machine import UART, Pin
import micropyGPS
import time

# Initialize GPS
uart = UART(1, baudrate=9600, tx=14, rx=34)  # Update pins according to your hardware setup
my_gps = micropyGPS.MicropyGPS()

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
            # print('Satellites in View:', my_gps.satellites_in_view)
            # print('Satellites in Use:', my_gps.satellites_in_use)
            # print('Time Since Last Fix:', my_gps.time_since_fix())
        else:
            print("Waiting for GPS fix...")
            print("Raw GPS data:", my_sentence)

        # Optional: Log GPS data
        # my_gps.start_logging('gps_log.txt')
        # my_gps.write_log(my_sentence)
        # my_gps.stop_logging()

    else:
        print("No data from GPS module.")

    time.sleep(1)  # Adjust the sleep time as needed

