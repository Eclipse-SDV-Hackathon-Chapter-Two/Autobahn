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
from decision_functions import IsPointInROI
from utils import reorganize_yolo_json, bbox_centerpoint

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

global_result_set = []

# Callback for receiving messages
def object_raw_sub_callback(topic_name, msg, time):
    global global_result_set
    try:
        json_msg = json.loads(msg)
        global_result_set = reorganize_yolo_json(json_msg)
        
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    logger.info("Starting example app...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Is people in roi App")

    # Create a subscriber that listens on the "object_detection"
    sub = StringSubscriber("object_detection")
    # Set the Callback
    sub.set_callback(object_raw_sub_callback)


    # Create a publisher that listens on the "object_detection_class"
    pub = StringPublisher("people_in_roi")

    # Just don't exit
    try:
        while ecal_core.ok():
            if global_result_set:
                result_set = global_result_set  # Only publish if we have received class IDs
                for entry in result_set:
                    class_id, confidence, bbox = entry
                    center_x, below_y =  bbox_centerpoint(bbox)
                    center_below_point = (center_x, below_y)

                    if IsPointInROI(center_below_point, roi_points = [(0, 600),(0, 350), (450, 250), (550, 250), (1100, 720)]) is True \
                        and confidence > 0.1:
                        in_roi_msg = 1
                        pub.send(in_roi_msg)
                        # logger.info(f"Published: {in_roi_msg}")
                    else:
                        in_roi_msg = 0
                        pub.send(in_roi_msg)
                
            else:
                in_roi_msg = 0
                pub.send(in_roi_msg)
                # logger.info("No class IDs to publish yet.")

            # Wait before the next loop
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
        # logger.info("Application stopped by user.")

    
    # finalize eCAL API
    ecal_core.finalize()