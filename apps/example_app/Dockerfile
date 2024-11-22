FROM ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/ecal_base:5.12

WORKDIR /usr/src/app

COPY ecal.ini /etc/ecal/
COPY requirements.txt ./
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

