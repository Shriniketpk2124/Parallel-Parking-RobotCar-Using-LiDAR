from gpiozero import Motor
from time import sleep

right_motor = Motor(17, 22, 18)
left_motor = Motor(4, 24, 19)

def check_and_turn():
    try:
        with open("Task3_status.txt", "r") as file: 
            status = file.read().strip()
        print(f"Read status: {status}")

        if status == "Stop":
            print("Turning right...")
            right_motor.forward(0) 
            left_motor.forward(0.45) 
            sleep(0.5)
            right_motor.stop()
            left_motor.stop()
            print("Right turn completed.")

            with open("Task3_status.txt", "w") as file:
                file.write("Turn right completed")
            print("Written 'Turn right completed' to file.")

    except FileNotFoundError:
        print("Error: Task3_status.txt file not found. Please ensure the file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print('Stopping Interrupted.')
        quit()

check_and_turn()
