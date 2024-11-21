import math

def calculate_signed_angle(data):
    a = (500, 350)
    b = (420, 670)
    c = (x, y)

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



signed_angle_abc = calculate_signed_angle(x, y)
print(f"각도: {signed_angle_abc:.2f}도")
