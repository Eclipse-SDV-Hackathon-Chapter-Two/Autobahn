# **Autobahn - Shift to SDV**
## 🚗 Racing Towards a Safer SDV World

---

## **1. Introduction**
Our team, **Autobahn**, participated in the [Eclipse SDV Hackathon](https://www.eclipse-foundation.events/event/EclipseSDVHackathon/summary) under the **"Shift to SDV"** challenge.

The name **Autobahn** represents not only the ideal road for speed but also one of the safest highways in the world. It reflects our dual mission:

- To strive for a safer world of Software-Defined Vehicles (SDVs).
- To race ahead with innovative solutions in this hackathon.

<div align="center">
  <img src="https://github.com/user-attachments/assets/6848f11b-7e0e-4219-bb04-facca2ddc5b8" alt="Autobahn"/>
</div>

## **2. Problem Statement**
### 🌍 Enhancing Safety in Blind Spots and High-Risk Areas

One of the critical challenges for SDVs is ensuring safety by effectively detecting their surroundings. We focused on addressing situations where pedestrians or cyclists in blind spots could pose serious risks.

### **Our project tackles the following scenarios:**

#### **1. Blind Spots:**
- Pedestrians hidden behind parked vehicles can be difficult for moving cars to detect.
- Our solution activates **indicators**, **emergency lights**, or even sends information to other vehicles using **V2X communication** to alert drivers.


<div align="center">
  <img src="https://github.com/user-attachments/assets/a92fb23f-d7d0-4274-b31d-75407f622218" alt="accident" width="600"/>
</div>

#### **2. Children in School Zones:**
- Sudden appearances of children or people in blind spots are detected.
- A **red warning light** is displayed on the cluster to indicate potential danger.  
*(Not just limited to school zones, but in any area, the system detects pedestrians entering a specific ROI and highlights their direction with a red warning to ensure safety.)*



---

## **3. Our Solution**
### 🛠 Key Features

#### 🚶‍♂️ **Surrounding Detection:** 🚶‍♂️
- Real-time detection of pedestrians and cyclists in blind spots with YOLO.
- Notification systems to warn nearby vehicles.

#### 🚨 **Visual and Communication Alerts:** 🚨
- Activates visual alerts (indicators, emergency lights).
- Sends V2X messages for vehicle-to-vehicle communication.

#### 🌐 **OTA Updates:** 🌐
- Demonstrates how these functionalities can be delivered through Over-the-Air (OTA) updates.

---

## **4. How It Works**
### 🌀 System Flow

Our solution is divided into **Feature Parts** and **Connectivity Parts**, emphasizing three key functionalities:

<div align="center">
  <img src="diagrams/context.drawio.svg" alt="Context View" width="600"/>
</div>



### Feature Parts ###
#### **1. Detection:**
- Pedestrians or cyclists entering the vehicle's ROI (Region of Interest) are detected using a **YOLO model**.
- The system displays a **red warning light** on the cluster to indicate the pedestrian's direction, ensuring safety.  
*(This functionality is not limited to school zones but applies to all roads.)*

<div align="center">
  <img src="https://github.com/user-attachments/assets/9b8d8486-0096-4270-a50d-f26409a33ec6" alt="Detect_pedestrian" width="500"/>
</div>

#### **2. Alerts:**
- When the vehicle creates blind spots due to parked positions, the other vehicle mitigates potential dangers:
  - **Indicators** or **emergency lights** are activated to alert nearby drivers.
  - This ensures that other drivers can anticipate pedestrians in front of such vehicles and drive cautiously.
  - Additionally, the system sends this information to nearby vehicles using **V2X communication** for proactive safety.

<div align="center">
  <img src="https://github.com/user-attachments/assets/1fa460ea-dbde-4a7e-819f-68be766878de" alt="alert" width="400"/>
</div>

### Connectivity Parts ###
#### **3. Updates:**
- The system supports **Over-the-Air (OTA) updates**:
  - The vehicle communicates with an **AWS server** to check for available updates.
  - If a new version is available, the vehicle owner is notified.
  - Upon approval from the owner, the system performs the upgrade seamlessly, ensuring the latest features are applied.

<div align="center">
  <img src="https://github.com/user-attachments/assets/d98f79ff-5309-44a4-a203-26752f9d0f89" alt="OTA-AI" width="500"/>
</div>
<div align="center">
  <img src="https://github.com/user-attachments/assets/0efd8f92-9c2a-4917-93e2-b6471d8d5727" alt="OTA" width="500"/>
</div>
<div align="center"> OTA Architecture
<div align="center">
  <img src="https://github.com/user-attachments/assets/1eb2c8f6-8583-4c65-b5a7-c8ddc05be7c7" alt="OTAGIF" width="500"/>
</div>
<div align="center"> OTA Simulation
  
---

## **5. Technologies Used**
Our project leverages cutting-edge tools and frameworks to achieve our goals:

### **Core Technologies**
1. **[Ankaios](https://eclipse-ankaios.github.io/ankaios/latest/):**
   - An embedded container and workload orchestrator targeted at automotive HPCs

2. **[eCAL](https://projects.eclipse.org/projects/automotive.ecal):**
   - High-performance communication framework for inter-process messaging.
   - Fast communication middleware following the pub-sub principle
   - Enables fast and reliable data sharing between components.

3. **[Symphony](https://github.com/eclipse-symphony/symphony/tree/main/docs):**
   - Advanced orchestration and service discovery for SDV ecosystems.
   - Facilitates efficient interaction between vehicle systems and external services.

4. **[MQTT](https://mqtt.org/):**
   - A lightweight messaging protocol ideal for IoT and V2X communication.
   - Optimized for low-latency and reliable message delivery in dynamic network environments.

5. **[AWS](https://aws.amazon.com/):**
   - A comprehensive cloud computing platform providing scalable storage and computing services.
   - Ensures secure and efficient management of OTA updates for SDV systems.


## **6. Architecture**

### 🏗 Overview Diagram

<div align="center">
  <img src="https://github.com/user-attachments/assets/3a18bdf7-e928-4b56-9a66-6de6388bb336" alt="architecture" width="500"/>
</div>

The name of Decision Maker's workload is "example_app"

---

# How To Use

### Calculate Angle
Our camera's recording environment is not always perfectly aligned with the ground. Therefore, we need to build a system capable of predicting the direction of objects in any environment.

<div align="center">
  <img src="https://github.com/user-attachments/assets/23533fcc-9946-44ce-b59e-807040ead130" alt="angle" width="550"/>
</div>

In cases where the recording environment is misaligned, we create a reference line in the middle of the road using two points \(a\) and \(b\) (e.g., \(a(500, 350)\), \(b(420, 670)\) in the image above). The center of the target object is defined as point \(c\). 

Using our angle calculation algorithm, the object's direction is computed and sent to subscribers. If line \(bc\) is clockwise relative to \(ab\), a positive value is sent; otherwise, a negative value is sent.

# Simulation
## Hidden Danger People

<div align="center">
  <img src="https://github.com/user-attachments/assets/cf6a7dfb-8557-488b-b5e4-45986418b0e0" alt="pedestrian" width="550"/>
</div>

<div align="center">video data

<div align="center">
  <img src="https://github.com/user-attachments/assets/fc74eb59-ff97-442b-a2a2-67e086db110f" alt="redalert" width="550"/>
</div>
<div align="center">when person detected

<div align="center">
  <img src="https://github.com/user-attachments/assets/63bc5179-9094-4e27-8397-9e2503c353a3" alt="indicator" width="550"/>
</div>
<div align="center">Hidden dange people detected

<div align="center">
  <img src="https://github.com/user-attachments/assets/123080a8-6e7c-4001-87a0-426b62edcc5a" alt="warning_sign" width="550"/>
</div>
<div align="center">When received warning sign


# <div align="center">Developers</div>
### <div align="center">Connectivity Part</div>
<table align="center">

  <tr>
    <td align="center">
      <a href="https://github.com/jwoon0906">
        <img src="https://github.com/jwoon0906.png" width="150px;" alt="Jang-Woon Park"/>
        <br />
        <sub><b>Jang-Woon Park</b></sub>
      </a>
      <br />
      <a href="https://github.com/jwoon0906"><img src="https://img.shields.io/badge/GitHub-jwoon0906-blue?logo=github" alt="GitHub Badge" /></a>
      <br />
    </td>
    <td align="center">
      <a href="https://github.com/johook">
        <img src="https://github.com/johook.png" width="150px;
        " alt="Seok-Hun Cho"/>
        <br />
        <sub><b>Seok-Hun Cho</b></sub>
      </a>
      <br />
      <a href="https://github.com/johook"><img src="https://img.shields.io/badge/GitHub-johook-blue?logo=github" alt="GitHub Badge" /></a>
      <br />
    </td>
    
  </tr>
</table>

### <div align="center">Feature Part</div>
<table align="center">

  <tr>
    <td align="center">
      <a href="https://github.com/euiseok-shin">
        <img src="https://github.com/euiseok-shin.png" width="150px;" alt="Eui-Seok Shin"/>
        <br />
        <sub><b>Eui-Seok Shin</b></sub>
      </a>
      <br />
      <a href="https://github.com/euiseok-shin"><img src="https://img.shields.io/badge/GitHub-euiseokshin-blue?logo=github" alt="GitHub Badge" /></a>
      <br />
    </td>
    <td align="center">
      <a href="https://github.com/KunhoPark-Jason">
        <img src="https://github.com/KunhoPark-Jason.png" width="150px;" alt="Kun-Ho Park"/>
        <br />
        <sub><b>Kun-Ho Park</b></sub>
      </a>
      <br />
      <a href="https://github.com/KunhoPark-Jason"><img src="https://img.shields.io/badge/GitHub-KunhoParkJason-blue?logo=github" alt="GitHub Badge" /></a>
      <br />
    </td>
    
  </tr>
</table>

### <div align="center">UI Design</div>
<table align="center">

  <tr>
    <td align="center">
      <a href="https://github.com/junspring">
        <img src="https://github.com/junspring.png" width="150px;" alt="Jun-Beom Jung"/>
        <br />
        <sub><b>Jun-Beom Jung</b></sub>
      </a>
      <br />
      <a href="https://github.com/junspring"><img src="https://img.shields.io/badge/GitHub-junspring-blue?logo=github" alt="GitHub Badge" /></a>
      <br />
    </td>
  </table>
