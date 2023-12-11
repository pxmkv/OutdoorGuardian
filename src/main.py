import os
import time
import urandom
import micropyGPS
import json
import uasyncio as asyncio
from machine import I2S,Pin,SDCard,I2C,SPI,UART
import ssd1306
import _thread
import network
import espnow
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM, MAX30105_PULSE_AMP_LOWEST
from time import sleep
from lora import LoRa
import math
from QMC5883 import QMC5883L

#config
# sd = SDCard(slot=3)  # sck=18, mosi=23, miso=19, cs=5
# os.mount(sd, "/sd")
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
compass = QMC5883L(scl=22, sda=21)

display.invert(1)

display.text("  OUTDOOR", 0, 10, 1)
display.text("      GUARDIAN", 0, 20, 1)
display.text("    Group 6", 0, 50, 1)
display.show()

btn   = Pin(35,Pin.IN,Pin.PULL_UP)


#Heart rate initialization
heart = MAX30102(i2c=i2c)  # An I2C instance is required
heart.setup_sensor()
heart.set_sample_rate(400)
heart.set_fifo_average(8)
heart.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)

# Initialize GPS
uart = UART(1, baudrate=9600, tx=14, rx=34)  # Update pins according to your hardware setup
my_gps = micropyGPS.MicropyGPS()
data = [[13, 50, 25.0], 37.8752, -122.2577]
last_saved= [[13, 50, 25.0], 37.8757, -122.2587]


# Wifi initialization
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()


# SPI pins
SCK  = 5
MOSI = 27
MISO = 19
CS   = 18
RX   = 26
# Setup SPI
spi = SPI(
    1,
    baudrate=10000000,
    sck=Pin(SCK, Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(MOSI, Pin.OUT, Pin.PULL_UP),
    miso=Pin(MISO, Pin.IN, Pin.PULL_UP),
)
spi.init()
# Setup LoRa
lora = LoRa(
    spi,
    cs=Pin(CS, Pin.OUT),
    rx=Pin(RX, Pin.IN),
    frequency=915.0,
    bandwidth=250000,
    spreading_factor=10,
    coding_rate=5,
)



def disp():
    display.fill(0)
    display.text(buf[0], 0, 0, 1)
    display.text(buf[1], 0, 10, 1)
    display.text(buf[2], 0, 20, 1)
    display.text(buf[3], 0, 30, 1)
    display.text(buf[4], 0, 40, 1)
    display.text(buf[5], 0, 50, 1)
    display.show()

has_message=False    

wav_samples = bytearray(10000)

def play():
    global wav_samples
    audio_out = I2S(
        1,
        sck=Pin(4),
        ws=Pin(25),
        sd=Pin(0),
        mode=I2S.TX,
        bits=16,
        format=I2S.STEREO,
        rate=11000,
        ibuf=10000,
    )
    wav = open('recv.wav', "rb")
    _ = wav.seek(44)  # advance to first byte of Data section in WAV file
    # allocate sample array
    # memoryview used to reduce heap allocation
    wav_samples_mv = memoryview(wav_samples)
    # continuously read audio samples from the WAV file
    # and write them to an I2S DAC
    print("==========  START PLAYBACK ==========")
    try:
        while True:
            num_read = wav.readinto(wav_samples_mv)
            # end of WAV file?
            if num_read == 0:
                # end-of-file, advance to first byte of Data section
                _ = wav.seek(44)
                break
            else:
                _ = audio_out.write(wav_samples_mv[:num_read])
    except (KeyboardInterrupt, Exception) as e:
        print("caught exception {} {}".format(type(e).__name__, e))

    # cleanup
    wav.close()
    audio_out.deinit()
    print("Done")




def send_file(file_path):
    with open(file_path, 'rb') as f:
        while True:
            datas = f.read(50)  # ESP-NOW data limit per transmission
            if not datas:
                break
            e.send(peer, datas)



def calculate_bearing(coord1, coord2):
    """
    Calculate the bearing from coord1 to coord2 in degrees.

    Parameters:
    coord1 (tuple): A tuple containing the latitude and longitude of the first location (lat1, lon1)
    coord2 (tuple): A tuple containing the latitude and longitude of the second location (lat2, lon2)

    Returns:
    float: Bearing in degrees from North
    """
    lat1, lon1 = coord1[1], coord1[2]
    lat2, lon2 = coord2[1], coord2[2]

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Calculate bearing
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(dlon))

    initial_bearing = math.atan2(x, y)

    # Convert bearing from radians to degrees
    initial_bearing = math.degrees(initial_bearing)

    # Normalize bearing to 0 <= bearing < 360
    bearing = (initial_bearing + 360) % 360

    return bearing

def haversine(coord1, coord2):
    # Radius of the Earth in km
    R =  6378137.0
    # Extract latitude and longitude from the coordinates
    lat1, lon1 = coord1[1], coord1[2]
    lat2, lon2 = coord2[1], coord2[2]

    # Convert coordinates from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c 
    return distance


def record():
    global wav_samples
    # ======= AUDIO CONFIGURATION =======
    WAV_FILE = "mic.wav"
    RECORD_TIME_IN_SECONDS = 8
    WAV_SAMPLE_SIZE_IN_BITS = 16
    FORMAT = I2S.MONO
    SAMPLE_RATE_IN_HZ = 22050
    # ======= AUDIO CONFIGURATION =======

    format_to_channels = {I2S.MONO: 1, I2S.STEREO: 2}
    NUM_CHANNELS = format_to_channels[FORMAT]
    WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
    RECORDING_SIZE_IN_BYTES = (
        RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS
    )


    def create_wav_header(sampleRate, bitsPerSample, num_channels, num_samples):
        datasize = num_samples * num_channels * bitsPerSample // 8
        o = bytes("RIFF", "ascii")  # (4byte) Marks file as RIFF
        o += (datasize + 36).to_bytes(
            4, "little"
        )  # (4byte) File size in bytes excluding this and RIFF marker
        o += bytes("WAVE", "ascii")  # (4byte) File type
        o += bytes("fmt ", "ascii")  # (4byte) Format Chunk Marker
        o += (16).to_bytes(4, "little")  # (4byte) Length of above format data
        o += (1).to_bytes(2, "little")  # (2byte) Format type (1 - PCM)
        o += (num_channels).to_bytes(2, "little")  # (2byte)
        o += (sampleRate).to_bytes(4, "little")  # (4byte)
        o += (sampleRate * num_channels * bitsPerSample // 8).to_bytes(4, "little")  # (4byte)
        o += (num_channels * bitsPerSample // 8).to_bytes(2, "little")  # (2byte)
        o += (bitsPerSample).to_bytes(2, "little")  # (2byte)
        o += bytes("data", "ascii")  # (4byte) Data Chunk Marker
        o += (datasize).to_bytes(4, "little")  # (4byte) Data size in bytes
        return o


    wav = open(WAV_FILE, "wb")

    # create header for WAV file and write to SD card
    wav_header = create_wav_header(
        SAMPLE_RATE_IN_HZ,
        WAV_SAMPLE_SIZE_IN_BITS,
        NUM_CHANNELS,
        SAMPLE_RATE_IN_HZ * RECORD_TIME_IN_SECONDS,
    )
    num_bytes_written = wav.write(wav_header)

    audio_in = I2S(
        0,
        sck=Pin(4),
        ws=Pin(25),
        sd=Pin(12),
        mode=I2S.RX,
        bits=WAV_SAMPLE_SIZE_IN_BITS,
        format=I2S.MONO,
        rate=SAMPLE_RATE_IN_HZ,
        ibuf=20000,
    )

    # allocate sample arrays
    # memoryview used to reduce heap allocation in while loop
    #mic_samples = bytearray(10000)
    mic_samples_mv = memoryview(wav_samples)

    num_sample_bytes_written_to_wav = 0

    print("Recording size: {} bytes".format(RECORDING_SIZE_IN_BYTES))
    print("==========  START RECORDING ==========")
    try:
        rec_time=0
        while not btn.value():
            # read a block of samples from the I2S microphone
            num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
            print(num_bytes_read_from_mic)
            if num_bytes_read_from_mic > 0:
                num_bytes_to_write = min(
                    num_bytes_read_from_mic, RECORDING_SIZE_IN_BYTES - num_sample_bytes_written_to_wav
                )
                # write samples to WAV file
                num_bytes_written = wav.write(mic_samples_mv[:num_bytes_to_write])
                num_sample_bytes_written_to_wav += num_bytes_written

        print("==========  DONE RECORDING ==========")
    except (KeyboardInterrupt, Exception) as e:
        print("caught exception {} {}".format(type(e).__name__, e))
    wav.close()
    audio_in.deinit()



    
def convert_to_decimal(loc):
    decimal = loc[0] + loc[1] / 60
    if loc[2] in ['S', 'W']:
        decimal = -decimal
    return decimal


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False



def get_packet():
    global last_saved
    try:    
        if uart.any():
            my_sentence = uart.readline().decode('utf-8')
            for x in my_sentence:
                my_gps.update(x)
            # Check if the data is valid
            if my_gps.valid:
                last_saved = [my_gps.timestamp, convert_to_decimal(my_gps.latitude), convert_to_decimal(my_gps.longitude)]
            else:        
                print("Waiting for GPS fix...")
        else:
            print("No data from GPS module.")
    except Exception as e:
        print(f"Error processing input: {e}")
    return last_saved

t_mode=False #tracking mode

buf=['PRESS TO SPEAK','','','','','']
last_pack_time = 0
last_rssi=''

def callback(pack):
    global t_mode,buf, data,last_pack_time, last_rssi
    print('lora_pack',pack)
    try:
        tmp=json.loads(pack.decode())
        data = tmp
        last_rssi=str(max(-lora.get_rssi()-43,0))
    except Exception as e:
        print(f"Error processing input: {e}")
    t_mode=True
    last_pack_time=time.ticks_ms()//1000

def send_location():
    heart.set_active_leds_amplitude(MAX30105_PULSE_AMP_LOWEST)
    display.invert(1)
    buf[3]='EMERGENCY'
    buf[4]='     MODE'
    disp()
    while True:
        lora.send(str(get_packet()))
        print('lora sent')
        sleep(0.5)


# lora.on_recv(callback)
def main():
    global buf
    while True:
        while True:
            if t_mode:    
                heart.set_active_leds_amplitude(MAX30105_PULSE_AMP_LOWEST)
                break
            heart.check()
            if heart.available() :
                ir  = heart.pop_ir_from_storage()
                if ir < 10000 or ir > 20000:
                    send_location()
            sleep(1)
        #tracking mode
        packs=get_packet()
        buf[2] = 'Dist ' + str(haversine(packs, data)) +' m'
        #buf[3] = 'Dir ' + str(calculate_bearing(packs, data)) + ' deg'

        dir_angle = compass.calculate_heading() - calculate_bearing(packs, data) 
        if dir_angle > 180:
            dir_angle -= 360
        elif dir_angle < -180:
            dir_angle += 360
        if abs(dir_angle)<30:
            display.invert(1)
        else:
            display.invert(0)
        if dir_angle <0:
            buf[3]= "Right " + str(abs(dir_angle))+ " degrees"
        else:
            buf[3]= "Left  " + str(dir_angle) + " degrees"
            
        buf[4] = "Compass " + str(compass.calculate_heading())
        buf[5] = "Bearing " + str(calculate_bearing(packs, data) )


        # buf[4] = 'Lora Dist ' + last_rssi 
        time_diff=time.ticks_ms()//1000-last_pack_time
        #buf[5]='RECD ' +str(time_diff) + 's ago'# update buffer
        disp() # show display
        sleep(0.2)#update every 0.2 second


def recv_audio():
    global has_message
    while True:
        with open('recv.wav', 'wb') as file:
            while True:
                host, msg = e.recv()
                if msg:
                    has_message=True
                    if msg == b'end':
                        break
                    file.write(msg)
                else:
                    sleep(0.2)#reduce loop time

        buf[0]='PLAYING'
        disp() 
        play()
        has_message=False
        buf[0]='PRESS TO SPEAK'
        disp() 
        
def send_audio():
    global has_message
    while True:
        if not btn.value() and not has_message:
            buf[0]='RECORDING'
            disp()
            record()
            buf[0]='SENDING'
            disp()    
            send_file('mic.wav')
            e.send(peer, b'end')
            buf[0]='PRESS TO SPEAK'
            disp() 
        else:
            sleep(0.1)#reduce loop time

# main program

if not btn.value():
    display.text("CALIBRATING", 0, 30, 1)
    display.show()    #calibration
    compass.calibrate(num_samples=200)
    print(compass.offset_x, compass.offset_y, compass.offset_z)
    

sleep(3)
display.invert(0)
disp()


lora.on_recv(callback)
lora.recv() #lora recv thread
audio_s_thread = _thread.start_new_thread(send_audio,())
audio_r_thread = _thread.start_new_thread(recv_audio,())
if __name__ == '__main__': # main thread
    main()






