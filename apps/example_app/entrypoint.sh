#!/bin/bash
# 진입 스크립트

# background로 ecal_play 실행
ecal_play -m ../../measurements/2024-11-20_17-43-12.696_measurement &

# 각 Python 스크립트를 백그라운드로 실행
python3 -u ./detect_in_roi.py &
python3 -u ./objectdetection_angle.py &
python3 -u ./objectdetection_arbiter.py &
python3 -u ./test.py &

# 모든 백그라운드 프로세스가 종료될 때까지 대기
wait