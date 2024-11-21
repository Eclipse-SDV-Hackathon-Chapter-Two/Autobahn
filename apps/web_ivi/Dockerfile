FROM ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/ecal_base:5.12

# 1. 필수 패키지 설치
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    protobuf-compiler \
    net-tools \
    curl \
    tar \
    unzip \
    # add your packages here
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# 2. AWS CLI 설치
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && ./aws/install && \
    rm -rf awscliv2.zip ./aws

# 3. eCAL 설정 파일 복사
COPY ecal.ini /etc/ecal/

# 4. Python 의존성 설치
COPY requirements.txt ./
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

# 5. 웹 서버 애플리케이션 복사
COPY main.py /web_ivi/main.py
COPY static /web_ivi/static

# 6. 업데이트 스크립트 복사
COPY update_handler.sh /update_handler.sh
COPY updates /web_ivi/updates
RUN chmod +x /update_handler.sh

# 7. 작업 디렉토리 설정
WORKDIR /web_ivi

# 8. Entrypoint 설정
ENTRYPOINT ["bash", "/update_handler.sh"]
