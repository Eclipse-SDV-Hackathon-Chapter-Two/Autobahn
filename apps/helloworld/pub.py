BROKER_ADDRESS = "test.mosquitto.org"  # 공개 테스트 브로커
import paho.mqtt.client as mqtt
import time

PORT = 1883
TOPIC = "test/shshsh"

def publish_message():
    # 클라이언트 생성
    client = mqtt.Client()

    # 브로커 연결
    client.connect(BROKER_ADDRESS, PORT, 60)

    # 메시지 발행
    message = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    for _ in range(20):
        client.publish(TOPIC, message)
        print(f"Message sent: {message}")
        time.sleep(1)

    # 연결 종료
    client.disconnect()

if __name__ == "__main__":
    publish_message()
