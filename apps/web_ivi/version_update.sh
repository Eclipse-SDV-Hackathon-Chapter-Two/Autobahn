#!/bin/bash

# S3 설정
BUCKET_NAME="sdvhackathon-autobahn-simpleota"
LATEST_VERSION_URL="https://${BUCKET_NAME}.s3.us-east-1.amazonaws.com/latest_version.txt"
UPDATE_URL_BASE="https://${BUCKET_NAME}.s3.us-east-1.amazonaws.com"
UPDATE_DIR="updates"
LOCAL_VERSION_FILE="$UPDATE_DIR/current_version.txt"
TEMP_FILE="$UPDATE_DIR/update.zip"
echo "version update.sh Start ..."
LATEST_VERSION=$(curl -s "$LATEST_VERSION_URL")

# 업데이트 파일 다운로드
curl -s -o "$TEMP_FILE" "$UPDATE_URL_BASE/$LATEST_VERSION/static.zip"

if [ $? -ne 0 ]; then
  echo "Failed to download update from S3"
  exit 1
fi
# 업데이트 적용
unzip "$TEMP_FILE" -d /web_ivi/updates

echo "Update applied successfully. Starting server..."  
curl -X POST http://localhost:5960/ota
