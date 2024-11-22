# Copyright (c) 2024 Elektrobit Automotive GmbH and others

# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0

import sys, time, json, logging

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
from ecal.core.publisher import StringPublisher
from decision_functions import HiddenDangerPeople, IsPointInROI
from utils import reorganize_yolo_json, bbox_centerpoint, calculate_signed_angle
# import paho.mqtt.client as mqtt

# Logging setup
logger = logging.getLogger("example_app")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

# Class labels for object detection
CLASS_LABELS = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    6: "train",
    7: "truck",
    9: "traffic light",
    11: "stop sign",
    12: "parking meter",
}

global_result_set = []

# Callback for object detection messages
def object_raw_sub_callback(topic_name, msg, time):
    global global_result_set
    try:
        json_msg = json.loads(msg)
        global_result_set = reorganize_yolo_json(json_msg)
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

# MQTT settings
BROKER_ADDRESS = "test.mosquitto.org"  # Public MQTT broker
PORT = 1883
TOPIC = "test/shshsh"

# Function to publish a warning message via MQTT
def publish_message():
    client = mqtt.Client()  # Create MQTT client
    client.connect(BROKER_ADDRESS, PORT, 60)  # Connect to the broker
    message = "warning"
    client.publish(TOPIC, message)  # Publish the message
    print(f"Message sent: {message}")

if __name__ == "__main__":
    logger.info("Starting example app...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Object_Detection_arbiter")

    # Subscriber for object detection
    sub = StringSubscriber("object_detection")
    sub.set_callback(object_raw_sub_callback)

    # Publisher for hidden danger status
    pub_hidden_danger_people = StringPublisher("hidden_danger_people")

    try:
        while ecal_core.ok():
            if global_result_set:
                result_set = global_result_set  # Use only if we received valid data

                # Check for hidden danger and publish status
                if HiddenDangerPeople(result_set) == "danger":  # Example condition
                    pub_hidden_danger_people.send("HiddenDangerPeople")

                    # Log inspection
                    # logger.info("HiddenDangerPeople")

                else:
                    pub_hidden_danger_people.send("Safe")

                    # Log inspection
                    # logger.info("No class IDs to publish yet.")

            else:
                pub_hidden_danger_people.send("Safe")  # Default to safe

                # Log inspection
                # logger.info("No class IDs to publish yet.")

            # Wait before next iteration
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    # Finalize eCAL API
    ecal_core.finalize()
