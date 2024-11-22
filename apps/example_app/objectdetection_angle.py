import sys
import time
import json
import math
import logging

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
from ecal.core.publisher import StringPublisher

logger = logging.getLogger("example_app")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

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

global_result_set = []
people_roi_topic = "Safe"

def object_raw_sub_callback(topic_name, msg, time):
    global global_result_set
    try:
        json_msg = json.loads(msg)
        class_ids = json_msg.get("class_ids", [])
        confidences = json_msg.get("confidences", [])
        xyxy = json_msg.get("xyxy", [])

        global_result_set = []

        for i, class_id in enumerate(class_ids):
            global_result_set.append([class_ids[i], confidences[i], xyxy[i]])

    except Exception as e:
        logger.error(f"Error: {e}")

def people_in_roi_callback(topic_name, msg, time):
    global people_roi_topic
    people_roi_topic = msg.strip()

if __name__ == "__main__":
    logger.info("Starting example app...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Angle Calculation App")

    # Create a subscriber for "object_detection"
    sub = StringSubscriber("object_detection")
    sub.set_callback(object_raw_sub_callback)
    
    sub_roi = StringSubscriber("people_in_roi")
    sub_roi.set_callback(people_in_roi_callback)

    # Create a publisher for "calculated_angle"
    pub = StringPublisher("calculated_angle")

    # Run the application
    try:
        while ecal_core.ok():
            if global_result_set:
                for entry in global_result_set:
                    class_id, confidence, bbox = entry
                    if class_id == 0.0 and confidence >= 0.5 and people_roi_topic == "PeopleInRoi":
                        x1, y1, x2, y2 = bbox
                        c = ((x1 + x2) / 2, (y1 + y2) / 2)

                        angle = calculate_signed_angle(a, b, c)
                        pub.send(str(int(angle)))
                        
                        # Log inspection
                        #logger.info(f"Published angle: {angle:.2f}")

                    else:
                        pub.send("Safe")

                        # Log inspection
                        #logger.info("Obeject detected but Safe")
                        
            else:
                pub.send("Safe")

                # Log inspection
                # logger.info("No Object")
                                
            global_result_set = []

            # Wait before the next loop
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    # finalize eCAL API
    ecal_core.finalize()
