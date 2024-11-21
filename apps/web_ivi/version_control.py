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
    if msg == "1": # yes
        subprocess.run(["bash", "version_update.sh"])
        print("Update Start ...")
        
    else:
        print("Update Pass")



if __name__ == "__main__":

    # Publish part
    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Version Control")

    # Create a publisher that sends dummy data to the "hello_topic" topic
    pub = StringPublisher("version")
    yorn_sub = StringSubscriber("yorn")
    
    # Subscribe part
    yorn_sub.set_callback(callback)

    for i in range(10):
        pub.send("-1")
        time.sleep(0.1)
    

    

    time.sleep(15) #15s wait

    # finalize eCAL API
    ecal_core.finalize()