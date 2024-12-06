from gpiozero import Motor
from time import sleep
from math import floor
from adafruit_rplidar import RPLidar

# ------------------- Configuration -------------------
PORT_NAME = '/dev/ttyUSB0'
ALIGNMENT_ANGLE_RANGE = 20  # Degrees to check on either side of forward
ALIGNMENT_THRESHOLD = 20   # Distance difference threshold in mm

# ------------------- Setup ---------------------------
right_motor = Motor(17, 22, 18)
left_motor = Motor(4, 24, 19)
lidar = RPLidar(None, PORT_NAME)

def check_alignment(scan_data):
    left_distances, right_distances = [], []
    for angle in range(0, 20):
        left_distances.append(scan_data[angle])

    for angle in range(340, 360):
        right_distances.append(scan_data[angle])

    # If there's not enough data, consider it unknown (treat as tilted)
    if not left_distances or not right_distances:
        return False

    avg_left = sum(left_distances) / len(left_distances)
    avg_right = sum(right_distances) / len(right_distances)

    difference = abs(avg_left - avg_right)
    '''
    if difference < 20:
        if avg_left < avg_right:
            # Left side closer means we are angled towards left, rotate slightly right
            right_motor.forward(0)  # Keep right wheel going forward
            left_motor.forward(0.25)                # Left wheel stationary to pivot
            sleep(0.1) # Keep right wheel going forward
            left_motor.forward(0)
        else:
            # Right side closer means angled towards right, rotate slightly left
            left_motor.forward(0)   # Keep left wheel going forward
            right_motor.forward(0.25)               # Right wheel stationary to pivot
            sleep(0.1)
            right_motor.forward(0)
        '''
    return difference < 20

scan_data = [0]*360
try:
    with open("Task3_status.txt", "r") as file:  # Opens the file and automatically closes it after reading
        status = file.read().strip()
    #print(f"Read status: {status}")

    # Step 2: Perform a right turn if the status is "Stop"
    if status == "Turn left completed":
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                scan_data[min([359, floor(angle)])] = distance

            if check_alignment(scan_data):
                print("The car is aligned straight.")
                #right_motor.forward(0)#
                #left_motor.forward(0)
            else:
                print("The car appears tilted.")

except KeyboardInterrupt:
    print('Stoping.')
lidar.stop()
lidar.disconnect()
print("LiDAR Disconnected.")