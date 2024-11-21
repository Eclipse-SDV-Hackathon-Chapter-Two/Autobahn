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

def reorganize_yolo_json(json_msg):
    class_ids = json_msg.get("class_ids", [])
    confidences = json_msg.get("confidences", [])
    xyxy = json_msg.get("xyxy", [])

    ######초기화 타이밍 문제
    result_set = []

    for i, class_id in enumerate(class_ids):
        result_set.append([class_ids[i], confidences[i], xyxy[i]])
    return result_set
    
