from gpiozero import Motor
from time import sleep

# Motor setup
right_motor = Motor(17, 22, 18)
left_motor = Motor(4, 24, 19)

def check_and_turn():
    try:
        # Step 1: Read the status from the file
        with open("Task3_status.txt", "r") as file:  # Opens the file and automatically closes it after reading
            status = file.read().strip()
        #print(f"Read status: {status}")

        # Step 2: Perform a right turn if the status is "Stop"
        if status == "Stopped obstacle behind!":
            #print("Turning left...")
            right_motor.forward(0.40)  # Right motor stationary
            left_motor.forward(0)  # Left motor moves forward to create a right turn
            sleep(0.5)  # Adjust this duration as needed for the right turn
            right_motor.stop()
            left_motor.stop()
            #print("Right turn completed.")

            # Step 3: Update the status file to indicate the turn is completed
            with open("Task3_status.txt", "w") as file:  # Opens in write mode and closes automatically
                file.write("Turn left completed")
            #print("Written 'Turn left completed' to file.")

    except FileNotFoundError:
        print("Error: Task3_status.txt file not found. Please ensure the file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print('Stopping Interrupted.')
        quit()

# Call the function
check_and_turn()