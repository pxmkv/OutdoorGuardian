import machine
import time
from QMC5883 import QMC5883L

# Initialize I2C

magnetometer = QMC5883L(scl=25, sda=4)

# Function to check if sensor is connected
def check_sensor_connection():
    try:
        magnetometer.reset()
        print("Sensor connected successfully.")
    except Exception as e:
        print("Sensor connection failed:", e)

# Calibrate magnetometer
def calibrate_magnetometer():
    print("Starting calibration...")
    min_x, max_x, min_y, max_y = 0, 0, 0, 0

    for i in range(100):
        try:
            x, y, z = magnetometer.get_magnet()
            if i == 0:
                min_x, max_x, min_y, max_y = x, x, y, y
            else:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
        except Exception as e:
            print("Error reading from sensor:", e)
            return
        time.sleep(0.1)

    offset_x = (max_x + min_x) / 2
    offset_y = (max_y + min_y) / 2
    scale_x = 2 / (max_x - min_x)
    scale_y = 2 / (max_y - min_y)

    print("Calibration complete.")
    print("Offsets: x =", offset_x, ", y =", offset_y)
    print("Scales: x =", scale_x, ", y =", scale_y)

    return offset_x, offset_y, scale_x, scale_y

# Main function
def main():
    check_sensor_connection()
    calibrate_magnetometer()

main()

