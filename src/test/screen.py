from machine import Pin, I2C
import ssd1306
import time

# using default address 0x3C
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    display.text('Hello, World!', 0, 0, 1)
    display.show()
    time.sleep(1)
    display.fill(0)

    display.invert(1)

    display.text('Bruh', 0, 0, 1)
    display.show()
    time.sleep(1)
    display.fill(0)
    display.invert(0)

