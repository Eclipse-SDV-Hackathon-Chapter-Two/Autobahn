import math

def reorganize_yolo_json(json_msg):
    class_ids = json_msg.get("class_ids", [])
    confidences = json_msg.get("confidences", [])
    xyxy = json_msg.get("xyxy", [])

    ######초기화 타이밍 문제
    result_set = []

    for i, class_id in enumerate(class_ids):
        result_set.append([class_ids[i], confidences[i], xyxy[i]])
    return result_set

def bbox_centerpoint(data):
    bbox = data
    x1, y1, x2, y2 = bbox
    x_mid = (x1 + x2) / 2
    y_mid = (y1 + y2) / 2

    return x_mid, y_mid

a = (500, 350)
b = (420, 670)

def calculate_signed_angle(a, b, c):
    vector_ab = (a[0] - b[0], a[1] - b[1])
    vector_cb = (c[0] - b[0], c[1] - b[1])

    dot_product = vector_ab[0] * vector_cb[0] + vector_ab[1] * vector_cb[1]
    cross_product = vector_ab[0] * vector_cb[1] - vector_ab[1] * vector_cb[0]

    magnitude_ab = math.sqrt(vector_ab[0]**2 + vector_ab[1]**2)
    magnitude_cb = math.sqrt(vector_cb[0]**2 + vector_cb[1]**2)

    cos_angle = dot_product / (magnitude_ab * magnitude_cb)
    angle = math.degrees(math.acos(cos_angle))

    if cross_product < 0:
        angle = -angle

    return angle

    
