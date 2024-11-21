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

import sys, time, logging, subprocess

import ecal.core.core as ecal_core
from ecal.core.publisher import StringPublisher
from ecal.core.subscriber import StringSubscriber

def callback(topic_name, msg, time):
    if msg == "-1": # different
        print("Y/N")

        # Publish part
        for i in range(15):
            pub.send("1")
            time.sleep(1)
        
    else:
        print("Fail")



if __name__ == "__main__":
    # Create a publisher that sends dummy data to the "hello_topic" topic
    ecal_core.initialize(sys.argv, "Random Control")

    sub = StringSubscriber("version")
    pub = StringPublisher("yorn")

    # Subscribe part
    
    sub.set_callback(callback)

    
    

    

    # finalize eCAL API
    ecal_core.finalize()