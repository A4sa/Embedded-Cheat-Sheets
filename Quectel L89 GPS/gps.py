import serial
import pynmea2
import time
from math import radians, sin, cos, sqrt, atan2

# Open the serial port for communication with the GPS module
uart_port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)

def parse_nmea_sentence(sentence):
    # Parse NMEA sentence using pynmea2 library
    try:
        msg = pynmea2.parse(sentence)
        return msg
    except pynmea2.ParseError as e:
        print("Error parsing NMEA sentence: {}".format(e))
        return None

def calculate_speed(lat1, lon1, lat2, lon2, time_diff):
    # Check if any coordinate is None before proceeding
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 0.0

    # Calculate speed based on two GPS coordinates and time difference
    # Implement the Haversine formula for distance calculation
    R = 6371.0  # Radius of the Earth in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c  # Distance in kilometers

    speed = distance / time_diff if time_diff > 0 else 0  # Speed in km/h
    return speed

try:
    previous_latitude = None
    previous_longitude = None
    previous_time = time.time()

    while True:
        # Read NMEA sentence from the GPS module
        nmea_sentence = uart_port.readline().decode('utf-8', errors='replace')

        # Check if the sentence is valid
        if nmea_sentence.startswith('$GNGGA'):
            gps_data = parse_nmea_sentence(nmea_sentence)

            # Check if the sentence is parsed successfully and contains necessary fields
            if gps_data and hasattr(gps_data, 'latitude') and hasattr(gps_data, 'longitude'):
                # Extract latitude, longitude, altitude, time, and speed
                latitude = float(gps_data.latitude) if gps_data.latitude else None
                longitude = float(gps_data.longitude) if gps_data.longitude else None

                # Check if latitude or longitude is None before proceeding
                if latitude is None or longitude is None:
                    continue

                # Check if altitude is not None before converting
                altitude = float(gps_data.altitude) if gps_data.altitude else 0.0

                time_utc = gps_data.timestamp

                # Calculate time difference
                time_diff = time.time() - previous_time

                # Calculate speed
                speed = calculate_speed(
                    previous_latitude, previous_longitude, latitude, longitude, time_diff
                )

                # Update previous values for the next iteration
                previous_latitude = latitude
                previous_longitude = longitude
                previous_time = time.time()

                # Display the information on the screen (replace this with your desired display method)
                print(f"NMEA Sentence: {nmea_sentence.strip()}")
                print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}m")
                print(f"Time (UTC): {time_utc}")
                print(f"Speed: {speed} km/h")
                print("=" * 30)

except KeyboardInterrupt:
    uart_port.close()
    print("Program terminated by user.")
