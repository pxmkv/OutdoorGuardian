# The MIT License (MIT)
# Copyright (c) 2022 Mike Teachman
# https://opensource.org/licenses/MIT

# Purpose: Read audio samples from an I2S microphone and write to SD card
#
# - read 32-bit audio samples from I2S hardware, typically an I2S MEMS Microphone
# - convert 32-bit samples to specified bit size
# - write samples to a SD card file in WAV format
# - samples will be continuously written to the WAV file
#   until a keyboard interrupt (ctrl-c) is detected
#
# Blocking version
# - the readinto() method blocks until
#   the supplied buffer is filled

import os
from machine import Pin
from machine import I2S


from machine import SDCard
from machine import I2C
import ssd1306

# using default address 0x3C
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.invert(0)
display.text('Recording', 0, 0, 1)
display.show()




sd = SDCard(slot=3)  # sck=18, mosi=23, miso=19, cs=5
os.mount(sd, "/sd")

# ======= AUDIO CONFIGURATION =======
WAV_FILE = "mic.wav"
RECORD_TIME_IN_SECONDS = 5
WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO
SAMPLE_RATE_IN_HZ = 22_050
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


wav = open("/sd/{}".format(WAV_FILE), "wb")

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
    while num_sample_bytes_written_to_wav < RECORDING_SIZE_IN_BYTES:
        # read a block of samples from the I2S microphone
        num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)

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


display.fill(0)
display.invert(1)
display.text('Playing', 0, 0, 1)
display.show()

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
wav = open("/sd/{}".format(WAV_FILE), "rb")
_ = wav.seek(44)  # advance to first byte of Data section in WAV file

# allocate sample array
# memoryview used to reduce heap allocation
wav_samples = bytearray(10000)
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
        else:
            _ = audio_out.write(wav_samples_mv[:num_read])
except (KeyboardInterru25pt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

# cleanup
wav.close()
if os.uname().machine.count("PYBD"):
    os.umount("/sd")
elif os.uname().machine.count("ESP32"):
    os.umount("/sd")
    sd.deinit()
elif os.uname().machine.count("Raspberry"):
    os.umount("/sd")
    spi.deinit()
elif os.uname().machine.count("MIMXRT"):
    os.umount("/sd")
    sd.deinit()
audio_out.deinit()
print("Done")