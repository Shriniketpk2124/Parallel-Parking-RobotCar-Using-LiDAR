import os
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar
from gpiozero import Robot
from time import sleep

# Motor setup
robot = Robot(right=(17, 22, 18), left=(4, 24, 19))

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

# Used to scale data to fit on the screen
max_distance = 0

def read_status():
    """Read the status from the text file."""
    try:
        with open("Task3_status.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Status file not found. Assuming default.")
        return "Unknown"

def process_data(scan_data):
    global max_distance
    count = 0

    # Check distances in the angle range 0 to 30 degrees
    for angle in range(0, 30):
        distance = scan_data[angle]
        print(f"Angle: {angle}, Distance: {distance}")
        if distance > 0:
            max_distance = max(min(5000, distance), max_distance)
            if distance <= 150:  # Obstacle detected within 150 mm
                count += 1

    if count > 0:
        print("STOP")
        robot.backward(0)
        with open("Task3_status.txt", "w") as f:
            f.write("Stopped obstacle behind!")
        quit()
    else:
        print("Moving Backward")
        robot.backward(0.33)
        with open("Task3_status.txt", "w") as f:
            f.write("Start")

scan_data = [0] * 360

try:
    # Check status from file
    status = read_status()
    print(f"Current status: {status}")

    if status == "Turn right completed":
        print("Status verified. Proceeding with LiDAR processing...")

        # LiDAR scanning and processing
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                scan_data[min(359, floor(angle))] = distance
            process_data(scan_data)

    else:
        print("Status not 'Turn right completed'. Halting operation.")

except KeyboardInterrupt:
    print("Stopping due to keyboard interrupt.")

finally:
    lidar.stop()
    lidar.disconnect()
    print("LiDAR Disconnected.")