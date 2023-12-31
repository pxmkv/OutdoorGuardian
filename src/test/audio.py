import os
import time
import urandom
import uasyncio as asyncio
from machine import I2S,Pin,SDCard,I2C,SPI
import ssd1306
import _thread
import network
import espnow
from lora import LoRa
from time import sleep

#config
sd = SDCard(slot=3)  # sck=18, mosi=23, miso=19, cs=5
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)


btn   = Pin(35,Pin.IN,Pin.PULL_UP)


# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)

e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()






def record():
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
        ibuf=40000,
    )

    # allocate sample arrays
    # memoryview used to reduce heap allocation in while loop
    mic_samples = bytearray(10000)
    mic_samples_mv = memoryview(mic_samples)

    num_sample_bytes_written_to_wav = 0

    print("Recording size: {} bytes".format(RECORDING_SIZE_IN_BYTES))
    print("==========  START RECORDING ==========")
    try:
        rec_time=0
        display.fill(0)
        display.invert(0)
        display.text('Recording', 0, 0, 1)
        display.text(str(rec_time), 0, 10, 1)
        display.show()
        past=time.ticks_ms()
        while not btn.value():
            # read a block of samples from the I2S microphone
            num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
            print(num_bytes_read_from_mic)
            if time.ticks_ms()-past>=1000:
                past=time.ticks_ms()
                rec_time+=1
                display.fill(0)
                display.text('Recording', 0, 0, 1)
                display.text(str(rec_time), 0, 10, 1)
                display.show()
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
has_message=False

def send_file(file_path):
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(50)  # ESP-NOW data limit per transmission
            if not data:
                break
            e.send(peer, data)
            #time.sleep(0.0001)  # To avoid sending data too quickly

def play():
    audio_out = I2S(
        1,
        sck=Pin(4),
        ws=Pin(25),
        sd=Pin(0),
        mode=I2S.TX,
        bits=16,
        format=I2S.STEREO,
        rate=11025,
        ibuf=40000,
    )
    wav = open('mic.wav', "rb")
    _ = wav.seek(44)  # advance to first byte of Data section in WAV file
    # allocate sample array
    # memoryview used to reduce heap allocation
    wav_samples = bytearray(10000)
    wav_samples_mv = memoryview(wav_samples)
    display.fill(0)
    display.invert(1)
    display.text('Playing', 0, 0, 1)
    display.show()
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

def audio_thread():
    global has_message
    while True:
        if not btn.value():
            record()
            play()
            # send_file('mic.wav')
            # e.send(peer, b'end')
        # if has_message:
        #     has_message=False
            # Write the received chunk to the file
        display.fill(0)
        display.invert(0)
        display.text('PRESS TO SPEAK', 0, 0, 1)
        display.show()

thread1= _thread.start_new_thread(audio_thread, ())
"""
while True:
    with open("/sd/{}".format('recv.wav'), 'wb') as file:
        while True:
            host, msg = e.recv()
            if msg:
                # Check for the end of the file transmission
                if msg == b'end':
                    
                    break
                    
                # Write the received chunk to the file
                file.write(msg)
        play()
"""
#audio_thread()
