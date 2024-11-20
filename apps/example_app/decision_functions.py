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

def HiddenDangerPeople(data):
    """
    Process the filtered result and check conditions:
    - The first value in the list must be 0.0
    - The second value (confidence) must be >= 0.75
    - The midpoint of the x-coordinates (x1 + x2)/2 must be > 360

    If all conditions are met, return "WARNING". Otherwise, return "SAFE".
    """
    for entry in data:
        class_id, confidence, bbox = entry
        if class_id == 0.0 and confidence >= 0.75:
            x1, y1, x2, y2 = bbox
            x_mid = (x1 + x2) / 2
            if x_mid <= 640:
                return "danger"
    return "safe"
