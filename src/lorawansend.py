from time import sleep
import  ssd1306
import heartrate

def send(lora):
    counter = 0
    print("LoRa Sender")
    display = Display()

    while True:
        payload = 'Alert: Danger ({0})'.format(counter)
        display.show_text_wrap("{0} RSSI: {1}".format(payload, lora.packet_rssi()))
        lora.println(payload)

        counter += 1
        sleep(5)
def send_heartrate(lora):
    sensor = MAX30102(i2c=i2c)
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

    t_start = ticks_us()  # Starting time of the acquisition
    samples_n = 0  # Number of samples that have been collected

    while True:
        sensor.check()

        # Check if the storage contains available samples
        if sensor.available():
            # Access the storage FIFO and gather the readings (integers)
            red_reading = sensor.pop_red_from_storage()
            ir_reading = sensor.pop_ir_from_storage()

            # Print the acquired data (so that it can be plotted with a Serial Plotter)
            print(red_reading, ",", ir_reading)

            # Compute the real frequency at which we receive data
            if compute_frequency:
                if ticks_diff(ticks_us(), t_start) >= 999999:
                    f_HZ = samples_n
                    samples_n = 0
                    print("acquisition frequency = ", f_HZ)
                    t_start = ticks_us()
                else:
                    samples_n = samples_n + 1
            if(red_reading < 40):
                payload = 'Alert: Danger ({0})'.format(counter)
                display.show_text_wrap("{0} RSSI: {1}".format(payload, lora.packet_rssi()))
                lora.println(payload)

        counter += 1
        sleep(5)

if __name__ == '__main__':
    main()