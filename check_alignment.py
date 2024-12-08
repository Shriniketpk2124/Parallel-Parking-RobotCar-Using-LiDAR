from gpiozero import Motor
from time import sleep
from math import floor
from adafruit_rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'
ALIGNMENT_ANGLE_RANGE = 20  
ALIGNMENT_THRESHOLD = 20

right_motor = Motor(17, 22, 18)
left_motor = Motor(4, 24, 19)
lidar = RPLidar(None, PORT_NAME)

def check_alignment(scan_data):
    left_distances, right_distances = [], []
    for angle in range(0, 20):
        left_distances.append(scan_data[angle])

    for angle in range(340, 360):
        right_distances.append(scan_data[angle])

    if not left_distances or not right_distances:
        return False

    avg_left = sum(left_distances) / len(left_distances)
    avg_right = sum(right_distances) / len(right_distances)

    difference = abs(avg_left - avg_right)
    return difference < 20

scan_data = [0]*360
try:
    with open("Task3_status.txt", "r") as file:  
        status = file.read().strip()
    print(f"Read status: {status}")

    if status == "Turn left completed":
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                scan_data[min([359, floor(angle)])] = distance

            if check_alignment(scan_data):
                print("The car is aligned straight.")
            else:
                print("The car appears tilted.")

except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
print("LiDAR Disconnected.")
