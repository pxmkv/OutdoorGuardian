import math

def calculate_heading(x, y, declination=0):
    heading = math.atan2(y, x)
    heading_degrees = math.degrees(heading)
    heading_degrees += declination

    # Normalize to 0-360
    if heading_degrees < 0:
        heading_degrees += 360
    elif heading_degrees > 360:
        heading_degrees -= 360

    return heading_degrees

# Example usage
x, y, _, _, _ = sensor.read()  # Assuming sensor is an instance of your magnetometer class
declination = 10  # Example declination value
heading = calculate_heading(x, y, declination)
print("Heading:", heading, "degrees")
