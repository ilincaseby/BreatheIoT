<!-- # BreatheIoT 🌬️
IoT project with the purpose of controlling Xiaomi Smart Air Purifier 4 from distance while collecting data from it and show it on a screen(mobile/pc/laptop)

## Dependencies 🧩
    * python-miio for miiocli(necessary for scripts)
    * esptool
    * adafruit-ampy
    * docker
    * paho.mqtt
    * requests
    * threading
    * flutter

## Concept of working
    * You firstly need to set up you air purifier through the instructions presented on Xiaomi site. With first docker you need to find the token for your machine.
    * **By changing** ip and token in scripts you assure yourself that the local server works how it should work.
    * Running the docker in the code directory, you initiate a container that represents the broker reponsible for sharing data regarding commands and basic info to and from air purifier.
    * Uploading the code for esp32 on a board you set up the middle part between local server(who run the scripts and share commands) and the cloud services(also these need modified with your specific accounts).
    * When you upload the app from flutter to a PC/Phone, you need to make sure that also cloud services' ip are changed, along with username and password.
    * Short scheme: <Air Purifier> <-> Local Server <-> ESP32 <-> Cloud <-> App
    * Further details about implementation are present in *Documentation.pages* -->

# BreatheIoT 🌬️  
An IoT project aimed at **remotely controlling** the **Xiaomi Smart Air Purifier 4** while collecting real-time data and displaying it on a screen (mobile/PC/laptop).

---

## 🚀 **Overview**  
The system ensures seamless communication between the air purifier, a local server, an ESP32 microcontroller, and a cloud platform. The data flow enables monitoring air quality, controlling the purifier, and displaying information on a user-friendly Flutter app.

---

## 🧩 **Dependencies**  
To get started, make sure you have the following tools and libraries installed:

- **`python-miio`** → Used for `miiocli` (necessary for running scripts)  
- **`esptool`** → For flashing code to the ESP32 board  
- **`adafruit-ampy`** → File management for MicroPython devices  
- **`docker`** → To create the local MQTT broker container  
- **`paho-mqtt`** → Python MQTT client library for message transfer  
- **`requests`** → For HTTP API calls  
- **`threading`** → Enables running multiple processes in parallel  
- **`flutter`** → Mobile and desktop app interface  

---

## ⚙️ **How It Works**  

### **1. Initial Setup**  
- Follow the **Xiaomi Smart Air Purifier setup instructions** to connect the purifier to your network.  
- Use **Docker** and `miiocli` to retrieve the **IP address** and **device token** required for communication.

---

### **2. Configuring the System**  
Update the scripts with your **purifier's IP** and **token** to ensure the local server communicates properly with the air purifier.

---

### **3. Local MQTT Broker**  
Run a **Docker container** in the code directory to set up the **MQTT broker**. This broker acts as the communication hub, sharing data and commands between devices.

---

### **4. ESP32 Integration**  
- Flash the ESP32 board with the provided code using `esptool` or `ampy`.  
- The ESP32 acts as a **middleman** between the local server and cloud services, relaying information in both directions.

---

### **5. Flutter App Deployment**  
- Build and deploy the **Flutter application** on your PC or mobile device.  
- Update the app configurations (cloud IP, username, and password) to match your cloud service details.

---

### **6. Data Flow Overview**  
The data flow can be summarized as:  

> **Air Purifier** ↔ **Local Server** ↔ **ESP32** ↔ **Cloud Services** ↔ **Flutter App**

---

## 📄 **Short Summary**

The **BreatheIoT** project allows you to remotely control a **Xiaomi Smart Air Purifier 4** while collecting real-time data and displaying it on a mobile or desktop app.  

### 🔧 **How it Works**
1. **Set up the Air Purifier** following the official Xiaomi instructions and extract the **token** using the provided Docker tools.
2. **Configure Scripts**: Replace the **IP address** and **token** in the scripts to enable communication with the local server.
3. **Run the Local Server** using Docker. The server acts as a bridge to send commands and collect basic information.
4. **Upload ESP32 Code**: Flash the ESP32 board with the provided code. It acts as a middle layer between the local server and the cloud.
5. **Configure Cloud Services**: Update the cloud configurations with your specific accounts, including **username**, **password**, and **IP**.
6. **Deploy the App**: Build and upload the Flutter app to a mobile device or PC. Update the app's backend endpoints with the correct cloud details.
