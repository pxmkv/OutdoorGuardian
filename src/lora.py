from lora import lorawanreceive
from lora import lorawansend
from config import *
from machine import Pin, SPI
from sx127x import SX127x

device_spi = SPI(baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)

example = 'sender'

if __name__ == '__main__':
    if example == 'sender':
        lorawansend.send(lora)
    if example == 'receiver':
        lorawanreceive.receive(lora)

def main():
    # I2C software instance
    i2c = SoftI2C(sda=Pin(23),  # Here, use your I2C SDA pin
                  scl=Pin(22),  # Here, use your I2C SCL pin
                  freq=400000)  # Fast: 400kHz, slow: 100kHz

    # Examples of working I2C configurations:
    # Board             |   SDA pin  |   SCL pin
    # ------------------------------------------
    # ESP32 D1 Mini     |   22       |   21
    # TinyPico ESP32    |   21       |   22
    # Raspberry Pi Pico |   16       |   17
    # TinyS3			|	 8		 |    9

    # Sensor instance
    sensor = MAX30102(i2c=i2c)  # An I2C instance is required

    # Scan I2C bus to ensure that the sensor is connected
    if sensor.i2c_address not in i2c.scan():
        print("Sensor not found.")
        return
    elif not (sensor.check_part_id()):
        # Check that the targeted sensor is compatible
        print("I2C device ID not corresponding to MAX30102 or MAX30105.")
        return
    else:
        print("Sensor connected and recognized.")

    print("Setting up sensor with default configuration.", '\n')
    sensor.setup_sensor()

    
    sensor.set_sample_rate(400)
    sensor.set_fifo_average(8)
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)

    sleep(1)

    
    compute_frequency = True

    print("Starting data acquisition from RED & IR registers...", '\n')
    sleep(1)

    t_start = ticks_us()  
    samples_n = 0  
    counter = 0
    device_spi = SPI(baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(5, Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(27, Pin.OUT, Pin.PULL_UP),
        miso = Pin(19, Pin.IN, Pin.PULL_UP))
        
    lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)
    while True:
        sensor.check()

        if sensor.available():
            red_reading = sensor.pop_red_from_storage()
            ir_reading = sensor.pop_ir_from_storage()

            print(red_reading, ",", ir_reading)

            if compute_frequency:
                if ticks_diff(ticks_us(), t_start) >= 999999:
                    f_HZ = samples_n
                    samples_n = 0
                    print("acquisition frequency = ", f_HZ)
                    t_start = ticks_us()
                    lora.send(str(red_reading))
                    lora.send(str(ir_reading))
                else:
                    samples_n = samples_n + 1
                    
    
            

