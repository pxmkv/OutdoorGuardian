#inputs: pos1_lat, pos1_lon, pos2_lat, pos2_lon
#outputs: distance, direction relative to north

import math

def convert_to_decimal(degrees, minutes, direction):
    decimal = degrees + minutes / 60
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0

    # Convert coordinates from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def calculate_initial_compass_bearing(lat1, lon1, lat2, lon2):
    # Convert coordinates from degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    diff_long = math.radians(lon2 - lon1)

    x = math.sin(diff_long) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - (math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(diff_long))

    initial_bearing = math.atan2(x, y)

    # Convert bearing from radians to degrees
    initial_bearing = math.degrees(initial_bearing)

    # Normalize the bearing
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
    
def dist_and_dir(pos1_lat, pos1_lon, pos2_lat, pos2_lon):
    lat1 = convert_to_decimal(pos1_lat[0], pos1_lat[1], pos1_lat[2])
    lon1 = convert_to_decimal(pos1_lon[0], pos1_lon[1], pos1_lon[2])
    lat2 = convert_to_decimal(pos2_lat[0], pos2_lat[1], pos2_lat[2])
    lon2 = convert_to_decimal(pos2_lon[0], pos2_lon[1], pos2_lon[2])
    distance = haversine(lat1, lon1, lat2, lon2)
    direction = calculate_initial_compass_bearing(lat1, lon1, lat2, lon2)
    return (distance, direction)
    
    
    

pos1_lat = [40, 44.93, 'N'] 
pos1_lon = [73, 59.13, 'W']

pos2_lat = [51, 30.44, 'N']  
pos2_lon = [0, 7.68, 'W']



print(dist_and_dir(pos1_lat, pos1_lon, pos2_lat, pos2_lon))

