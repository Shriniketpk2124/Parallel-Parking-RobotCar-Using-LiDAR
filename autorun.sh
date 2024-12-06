#!/bin/bash

# Function to check if the previous script executed successfully
check_exit_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 did not terminate properly. Exiting..."
        exit 1
    fi
}

# Step 1: Run initial_wall_following.py
echo "Running shrinket_test.py..."
python3 "initial_wall_following.py"
check_exit_status "initial_wall_following.py"

# Step 2: Run turn_to_park.py
echo "Running turn_to_park.py..."
python3 "turn_to_park.py"
check_exit_status "turn_to_park.py"

# Step 3: Run reverse_into_parking_space.py
echo "Running reverse_into_parking_space.py..."
python3 "reverse_into_parking_space.py"
check_exit_status "reverse_into_parking_space.py"

# Step 4: Run final_parking_turn.py
echo "Running aligning_test_shriniket.py..."
python3 "final_parking_turn.py"
check_exit_status "final_parking_turn.py"

# Step 5: Run check_alignment.py
echo "Running trial_aligning.py..."
python3 "check_alignment.py"
check_exit_status "check_alignment.py"

echo "All scripts executed successfully!"