#!/bin/bash

# S3 설정
BUCKET_NAME="sdvhackathon-autobahn-simpleota"
LATEST_VERSION_URL="https://${BUCKET_NAME}.s3.us-east-1.amazonaws.com/latest_version.txt"
UPDATE_URL_BASE="https://${BUCKET_NAME}.s3.us-east-1.amazonaws.com"
UPDATE_DIR="updates"
LOCAL_VERSION_FILE="$UPDATE_DIR/current_version.txt"
TEMP_FILE="$UPDATE_DIR/update.tar.xz"

# 최신 버전 가져오기
LATEST_VERSION=$(curl -s "$LATEST_VERSION_URL")

if [ -z "$LATEST_VERSION" ]; then
  echo "Failed to fetch latest version from S3"
  exit 1
fi

# 로컬 버전 확인
if [ -f "$LOCAL_VERSION_FILE" ]; then
  LOCAL_VERSION=$(cat "$LOCAL_VERSION_FILE")
else
  LOCAL_VERSION="0.0.0"
fi

if [ "$LATEST_VERSION" == "$LOCAL_VERSION" ]; then
  echo "Already up-to-date. Starting server..."
  exec uvicorn main:app --host 0.0.0.0 --port 5959
fi

# 업데이트 파일 다운로드
curl -s -o "$TEMP_FILE" "$UPDATE_URL_BASE/$LATEST_VERSION/static.tar.xz"

if [ $? -ne 0 ]; then
  echo "Failed to download update from S3"
  exit 1
fi

# 업데이트 적용
tar -xJf "$TEMP_FILE" -C .  
echo "$LATEST_VERSION" > "$LOCAL_VERSION_FILE"

echo "Update applied successfully. Starting server..."
exec uvicorn main:app --host 0.0.0.0 --port 5959
