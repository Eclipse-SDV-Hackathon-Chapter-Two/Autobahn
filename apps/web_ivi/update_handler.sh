#!/bin/bash

# 설정: 최신 버전을 확인할 URL과 다운로드 경로
LATEST_VERSION_URL="http://example.com/updates/latest_version.txt"
BASE_UPDATE_URL="http://example.com/updates"
LOCAL_VERSION_FILE="/web_ivi/current_version.txt"
TEMP_DIR="/tmp/ota_update"
DOWNLOAD_FILE="$TEMP_DIR/update.tar.gz"

# 1. 현재 버전 확인
if [ -f "$LOCAL_VERSION_FILE" ]; then
    LOCAL_VERSION=$(cat "$LOCAL_VERSION_FILE")
else
    echo "Local version file not found. Assuming no updates applied."
    LOCAL_VERSION="0.0.0"
fi
echo "Current version: $LOCAL_VERSION"

# 2. 최신 버전 확인
LATEST_VERSION=$(curl -s "$LATEST_VERSION_URL")
if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch the latest version information."
    exit 1
fi
echo "Latest version: $LATEST_VERSION"

# 3. 버전 비교
if [ "$LOCAL_VERSION" == "$LATEST_VERSION" ]; then
    echo "No updates available. Exiting."
    exit 0
fi

# 4. 업데이트 파일 다운로드
echo "Downloading update for version $LATEST_VERSION..."
mkdir -p "$TEMP_DIR"
UPDATE_URL="$BASE_UPDATE_URL/$LATEST_VERSION/update.tar.gz"
curl -s -o "$DOWNLOAD_FILE" "$UPDATE_URL"

if [ $? -ne 0 ]; then
    echo "Error: Failed to download update file."
    exit 1
fi

# 5. 압축 해제 및 적용
echo "Applying update..."
tar -xzf "$DOWNLOAD_FILE" -C /web_ivi

if [ $? -ne 0 ]; then
    echo "Error: Failed to extract update file."
    exit 1
fi

# 6. 로컬 버전 파일 업데이트
echo "$LATEST_VERSION" > "$LOCAL_VERSION_FILE"
echo "Update to version $LATEST_VERSION applied successfully."

# 7. 정리
rm -rf "$TEMP_DIR"
