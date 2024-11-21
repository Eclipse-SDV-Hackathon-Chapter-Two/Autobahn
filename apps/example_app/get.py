import cv2

# 클릭 이벤트 콜백 함수 정의
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼 클릭
        print(f"클릭한 좌표: ({x}, {y})")

# 동영상 파일 경로 설정
video_path = '../../measurements/2024-11-19_15-45-14.870_measurement/video_out/2024-11-19_15-45-21_ts_det.mp4'  # 'your_video.mp4' 대신 동영상 파일 경로를 입력하세요.

# 동영상 캡처 객체 생성
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("동영상을 열 수 없습니다.")
    exit()

# OpenCV 창 이름 설정
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', click_event)

while True:
    ret, frame = cap.read()
    
    if not ret:  # 동영상 끝에 도달하면 루프 종료
        break

    cv2.imshow('Video', frame)

    # 키보드 입력 대기 ('q' 키를 누르면 종료)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()
