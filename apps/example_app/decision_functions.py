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

recent_x_mid = []

def HiddenDangerPeople(data):
    global recent_x_mid

    for entry in data:
        class_id, confidence, bbox = entry
        if class_id == 0.0 and confidence >= 0.5:
            x1, y1, x2, y2 = bbox
            x_mid = (x1 + x2) / 2

            if 0 <= x_mid <= 640:
                recent_x_mid.append(x_mid)
                if len(recent_x_mid) > 3:
                    recent_x_mid.pop(0)

                if len(recent_x_mid) == 3 and \
                   recent_x_mid[0] > recent_x_mid[1] > recent_x_mid[2]:
                    return "danger"
    return "safe"
