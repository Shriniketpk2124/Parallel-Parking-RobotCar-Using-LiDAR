from gpiozero import Motor
from time import sleep

right_motor = Motor(17, 22, 18)
left_motor = Motor(4, 24, 19)

def check_and_turn():
    try:
        with open("Task3_status.txt", "r") as file:
            status = file.read().strip()
        print(f"Read status: {status}")

        if status == "Stopped obstacle behind!":
            print("Turning left...")
            right_motor.forward(0.40)
            left_motor.forward(0)
            sleep(0.5)
            right_motor.stop()
            left_motor.stop()
            print("Right turn completed.")

            with open("Task3_status.txt", "w") as file:
                file.write("Turn left completed")
            print("Written 'Turn left completed' to file.")

    except FileNotFoundError:
        print("Error: Task3_status.txt file not found. Please ensure the file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print('Stopping Interrupted.')
        quit()

check_and_turn()
