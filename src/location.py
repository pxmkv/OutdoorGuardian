import math
from gps_module import read_gps  # Replace with your actual GPS module library and function
from lorawan_module import receive_lorawan  # Replace with your actual LoRaWAN module library and function

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def get_gps_data():
    # Function to get GPS data from your GPS module
    # Replace with actual code to read from your GPS module
    return read_gps()

def get_lorawan_data():
    # Function to get GPS data sent over LoRaWAN
    # Replace with actual code to read from your LoRaWAN receiver
    return receive_lorawan()

while True:
    # Read local GPS data
    local_lat, local_lon = get_gps_data()

    # Read remote GPS data from LoRaWAN
    remote_lat, remote_lon = get_lorawan_data()

    if local_lat is not None and local_lon is not None and remote_lat is not None and remote_lon is not None:
        # Calculate and print the distance
        distance = haversine(local_lat, local_lon, remote_lat, remote_lon)
        print(f"Distance: {distance:.2f} kilometers")

    # Add a delay or condition to wait for the next set of data
    # For example, sleep for a few seconds, or wait for a signal that new data is available
