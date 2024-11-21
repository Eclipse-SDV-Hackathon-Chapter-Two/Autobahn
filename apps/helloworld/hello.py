import paho.mqtt.client as mqtt

# 콜백 함수: 연결 성공 시 호출
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 연결 후 'test/topic'이라는 주제를 구독
    client.subscribe("test/shsh")

# 콜백 함수: 메시지 수신 시 호출
def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}\nMessage: {msg.payload.decode()}")

# MQTT 클라이언트 설정
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 브로커에 연결
client.connect("test.mosquitto.org", 1883, 60)

# 무한 루프 시작
client.loop_forever()
