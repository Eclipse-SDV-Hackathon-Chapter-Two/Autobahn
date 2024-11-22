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

global_result_set = []

# Callback for receiving messages
def object_raw_sub_callback(topic_name, msg, time):
    global global_result_set
    try:
        json_msg = json.loads(msg)
        global_result_set = reorganize_yolo_json(json_msg)
        
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

    # Create a publisher that listens on the "people_in_roi"
    pub = StringPublisher("people_in_roi")

    try:
        while ecal_core.ok():
            if global_result_set:
                for entry in global_result_set:
                    class_id, confidence, bbox = entry
                    center_x, below_y =  bbox_centerpoint(bbox)
                    center_below_point = (center_x, below_y)

                    if IsPointInROI(center_below_point, roi_points = [(0, 600),(0, 350), (450, 250), (550, 250), (1100, 720)]) and confidence >= 0.5:
                        pub.send("PeopleInRoi")

                        # Log inspection
                        # logger.info(f"Published: PeopleInRoi")
                    else:
                        pub.send("Safe")

                        # Log inspection
                        # logger.info("Object detected but Safe")
                
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