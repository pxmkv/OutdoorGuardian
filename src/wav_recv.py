import os
import network
import espnow
from machine import I2S,Pin,SDCard,I2C
import ssd1306

sd = SDCard(slot=3)  # sck=18, mosi=23, miso=19, cs=5
os.mount(sd, "/sd")
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

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
    wav = open("/sd/{}".format('recv.wav'), "rb")
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
            else:
                _ = audio_out.write(wav_samples_mv[:num_read])
    except (KeyboardInterrupt, Exception) as e:
        print("caught exception {} {}".format(type(e).__name__, e))

    # cleanup
    wav.close()

    audio_out.deinit()
    print("Done")

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

