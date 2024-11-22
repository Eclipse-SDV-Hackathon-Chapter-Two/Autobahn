#!/bin/bash
# Entry script

# Run each Python script in the background
python3 -u ./detect_in_roi.py &
python3 -u ./objectdetection_angle.py &

# Wait for all background processes to terminate
wait
