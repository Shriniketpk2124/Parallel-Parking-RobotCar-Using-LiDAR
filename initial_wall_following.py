import os
from math import cos, sin, pi, floor
#import pygame
from adafruit_rplidar import RPLidar
from gpiozero import Motor
from time import sleep, time

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
'''
pygame.init()
lcd = pygame.display.set_mode((720, 420))
pygame.mouse.set_visible(False)
lcd.fill((0, 0, 0))
pygame.display.update()
'''
# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

# Motor setup
right_motor = Motor(17, 22, 18)
left_motor = Motor(4, 24, 19)

# Used to scale data to fit on the screen
max_distance = 0
desired_distance_from_wall = 250  # Desired distance to maintain from the wall in mm
distance_tolerance = 50  # Tolerance in mm

# Parking detection variables
no_wall_start_time = None
parking_space_found = False
min_parking_space = 380  # Minimum space for parking in mm
robot_speed_mm_per_sec = 900  # Initial speed in mm/s
back_parking = False  # Variable to check if there is space behind

def is_parking_available(scan_data):
    distance = scan_data[135]
    if distance >= 100:
        print(f"Parking available, distance hori : {distance}")
        return True
    else:
        return False

def checking_wall_behind(scan_data):
    global back_parking
    for angle in range(30, 50):
        distance = scan_data[angle]
        if distance >= 420:
            back_parking = True
            print(f"checking wall behind, angle{angle}, distance{distance}")
            break
    else:
        back_parking = False

def wall_following_control(scan_data):
    global no_wall_start_time, parking_space_found, robot_speed_mm_per_sec, back_parking
    # Assume no wall detected initially
    wall_detected = False

    for angle in range(130, 140):
        distance = scan_data[angle]
        if distance > 0:
            if distance < desired_distance_from_wall + distance_tolerance:
                wall_detected = True
                break

    if wall_detected:
        # Wall detected: adjust motors to follow the wall
        print("Wall Detected, Following")
        no_wall_start_time = None  # Reset no wall detection timer
        right_motor.forward(speed=0.35)
        left_motor.forward(speed=0.35)
        with open("Task3_status.txt", "w") as f:
            f.write("Start")
            print("Written 'Start' to file")
        # Reset parking space found status
        parking_space_found = False
        back_parking = False

    else:
        # No wall detected
        print("No Wall Detected")

        if no_wall_start_time is None:
            no_wall_start_time = time()  # Start timer

        # Calculate the distance covered since the wall disappeared
        distance_covered = robot_speed_mm_per_sec * (time() - no_wall_start_time)

        # Check if both conditions are met: distance covered and space behind
        if distance_covered >= min_parking_space:
            checking_wall_behind(scan_data)  # Check if there is space behind

            if back_parking:
                parking_space_found = is_parking_available(scan_data)

                if parking_space_found:
                    right_motor.stop()
                    left_motor.stop()

                    with open("Task3_status.txt", "w") as f:
                        f.write("Stop")  # Write "Stop" if no wall is detected
                        print("Written 'Stop' to file")
                        exit()
                else:
                    print('horizontal parking space not enough!')

            else:
                print("checking parkings space behind !")
        else:
            print(f"calculating distance..")
'''
def process_data(scan_data):
    global max_distance
    #lcd.fill((0, 0, 0))
    for angle in range(360):
        distance = scan_data[angle]
        if distance > 0:  # Ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (400 + int(x / max_distance * 200), 180 + int(y / max_distance * 200))
            pygame.draw.circle(lcd, pygame.Color(255, 255, 255), point, 2)

    pygame.display.update()
'''
# Initialize scan data
scan_data = [0] * 360

try:
    #print(lidar.info)
    for scan in lidar.iter_scans():
        for item in scan:
            if len(item) == 3:
                _, angle, distance = item
            elif len(item) == 2:
                angle, distance = item
            else:
                continue

            if distance > 0:
                scan_data[min(359, floor(angle))] = distance

        #process_data(scan_data)
        wall_following_control(scan_data)

except KeyboardInterrupt:
    print('Stopping Interrupted.')
    quit()

finally:
    lidar.stop()
    lidar.disconnect()
    #pygame.quit()
    print("LiDAR Disconnected.")