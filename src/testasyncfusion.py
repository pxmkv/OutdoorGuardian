import uasyncio as asyncio
from machine import I2C, Pin 
from imu import MPU6050
from fusion_async import Fusion
import ssd1306

print("hello world")

# Pins according the schematic https://heltec.org/project/wifi-kit-32/
i2c_imu = I2C(-1, scl=Pin(25), sda=Pin(4))
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
imu = MPU6050(i2c_imu)

async def read_coro():
    print("read coro")
    # Assuming the imu object has methods for non-blocking retrieval of data
    imu.mag_trigger()  # Hardware dependent: trigger a nonblocking read
    await asyncio.sleep_ms(20)  # Wait for mag to be ready
    return imu.accel.xyz, imu.gyro.xyz, imu.mag_nonblocking.xyz  # Replace with actual methods to retrieve data

fuse = Fusion(read_coro)

async def display_orientation():
    print("display orientation")
    await fuse.start()  # Start the asynchronous update task
    while True:
        display.fill(0)  # Clear the display
        display.text('Pitch: {:.2f}'.format(fuse.pitch), 0, 0, 1)
        display.text('Yaw: {:.2f}'.format(fuse.heading), 0, 10, 1)
        # If you also want to display roll, uncomment the next line
        # display.text('Roll: {:.2f}'.format(fuse.roll), 0, 20, 1)
        display.show()
        await asyncio.sleep(0.5)  # Update interval

# Run the asynchronous loop
async def main():
    print("main")
    asyncio.create_task(display_orientation())
    # If you have other tasks to run, you can create them here

asyncio.run(main())
