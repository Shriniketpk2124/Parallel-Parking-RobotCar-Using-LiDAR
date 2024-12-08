#!/bin/bash

check_exit_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 did not terminate properly. Exiting..."
        exit 1
    fi
}

echo "Running shrinket_test.py..."
python3 "initial_wall_following.py"
check_exit_status "initial_wall_following.py"

echo "Running turn_to_park.py..."
python3 "turn_to_park.py"
check_exit_status "turn_to_park.py"

echo "Running reverse_into_parking_space.py..."
python3 "reverse_into_parking_space.py"
check_exit_status "reverse_into_parking_space.py"

echo "Running aligning_test_shriniket.py..."
python3 "final_parking_turn.py"
check_exit_status "final_parking_turn.py"

echo "Running trial_aligning.py..."
python3 "check_alignment.py"
check_exit_status "check_alignment.py"

echo "All scripts executed successfully!"
