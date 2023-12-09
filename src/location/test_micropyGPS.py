from machine import UART, Pin
import micropyGPS
import time
import json




# Initialize GPS
uart = UART(1, baudrate=9600, tx=17, rx=16)  # Update pins according to your hardware setup
my_gps = micropyGPS.MicropyGPS()


def str_to_array(string):
    if string != "":
        return eval(string)
    else:
        return string

    
def convert_to_decimal(loc):
    decimal = loc[0] + loc[1] / 60
    if loc[2] in ['S', 'W']:
        decimal = -decimal
    return decimal




def print_size_in_kb(data):
    serialized_data = json.dumps(data)
    size_in_bytes = len(serialized_data)
    size_in_kb = size_in_bytes / 1024
    print(f"Size: {size_in_kb:.2f} KB")


def get_packet():
    if uart.any():
        my_sentence = uart.readline().decode('utf-8')
        for x in my_sentence:
            my_gps.update(x)
            

        # Check if the data is valid
        if my_gps.valid:
            return str([my_gps.timestamp, convert_to_decimal(my_gps.latitude), convert_to_decimal(my_gps.longitude)])
            
        else:
            sample = [37, 52.51906, 'N']
            
            print("Waiting for GPS fix...")
            return ""
            # print("Raw GPS data:", my_sentence)
            #print(convert_to_decimal(sample))
            #print_size_in_kb(sample)
            #print_size_in_kb(convert_to_decimal(sample))

        # Optional: Log GPS data
        # my_gps.start_logging('gps_log.txt')
        # my_gps.write_log(my_sentence)
        # my_gps.stop_logging()

    else:
        print("No data from GPS module.")
        return ""



#while True:
#    print(get_packet())
#    time.sleep(1)  # Adjust the sleep time as needed

