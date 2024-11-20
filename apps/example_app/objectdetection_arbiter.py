# Copyright (c) 2024 Elektrobit Automotive GmbH and others

# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# SPDX-License-Identifier: Apache-2.0

import sys, time, json, logging

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
from ecal.core.publisher import StringPublisher

logger = logging.getLogger("example_app")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)


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

global_class_ids = []

# Callback for receiving messages
def object_raw_sub_callback(topic_name, msg, time):
    global global_class_ids
    try:
        json_msg = json.loads(msg)
        global_class_ids = json_msg.get("class_ids", [])
        # print(f"Received: {msg}")
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    logger.info("Starting example app...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Example App")

    # Create a subscriber that listens on the "object_detection"
    sub = StringSubscriber("object_detection")

    # Set the Callback
    sub.set_callback(object_raw_sub_callback)

    # Create a publisher that listens on the "object_detection_class"
    pub = StringPublisher("object_detection_class")
    
    class_ids = global_class_ids

    
    # Just don't exit
    try:
        while ecal_core.ok():
            if global_class_ids:  # Only publish if we have received class IDs
                pub.send(json.dumps({"class_ids": global_class_ids}))  # Send class_ids as JSON
                logger.info(f"Published: {global_class_ids}")
            else:
                logger.info("No class IDs to publish yet.")

            # Wait before the next loop
            time.sleep(0.1)

    except KeyboardInterrupt:
        logger.info("Application stopped by user.")

    
    # finalize eCAL API
    ecal_core.finalize()