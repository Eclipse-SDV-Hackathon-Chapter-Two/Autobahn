FROM ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/ecal_base:5.12

WORKDIR /usr/src/app

COPY ecal.ini /etc/ecal/
COPY requirements.txt ./
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

COPY detect_in_roi.py ./
COPY objectdetection_angle.py ./
COPY objectdetection_arbiter.py ./
COPY decision_functions.py ./
COPY utils.py ./

# 진입 스크립트 추가 및 실행 권한 부여
COPY entrypoint.sh /usr/src/app/
RUN chmod +x /usr/src/app/entrypoint.sh

# 진입 스크립트를 실행
CMD ["/usr/src/app/entrypoint.sh"]
