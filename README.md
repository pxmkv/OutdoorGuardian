# Outdoor Guardian: An Embedded Solution for Outdoor Enthusiasts

## Introduction

**Background:**  
In today's fast-paced world, people increasingly turn to outdoor activities such as hiking, skiing, and mountaineering to rejuvenate and reconnect with nature. Safety and communication are paramount during these adventures, especially in challenging terrains and unpredictable conditions.

**Project Overview:**  
The "Outdoor Guardian" is a cutting-edge embedded device designed to address these concerns. Tailored for outdoor enthusiasts, this gadget not only provides real-time tracking capabilities but also serves as a lifeline in times of need.

## Key Features:

1. **Real-time GPS Tracking:** Deliver accurate GPS positioning, ensuring adventurers always know their location.
2. **LoraWAN Communication:** Enables communication over long distances without traditional networks.
3. **Vital Sign Monitoring:** Tracks the user's vital signs in real-time.
4. **Emergency Alert System:** Sends out an immediate distress signal in emergencies.
6. **Long-lasting Battery:** Ensures users remain connected throughout their journey.

---

# Prototype Development for Outdoor Guardian

## 1. Project Background
Developing an embedded device with integrated functionalities for outdoor scenarios presents a broad application horizon.

## 2. Objectives & Specifications
- **Primary Goal**: Develop a prototype based on the ESP32 or Raspberry Pi platform.
- **Hardware Specifications**:
  - ESP32 or Raspberry Pi platform
  - GPS module
  - LoraWAN module
  - Heart rate sensor
  - Long-lasting battery
  - Buttons for input
  - IMU Sensor
## 3. Design & Development

### 3.1 Hardware Design
- Integration of ESP32 or Raspberry Pi with the necessary hardware modules.
- Power management for extended battery life.
- PCB layout design.

### 3.2 Software Development
- Using ESP-IDF or Raspbian for platform-specific firmware and drivers.
- Implementation of GPS tracking, LoraWAN communication, and health monitoring.

## 4. Prototype Validation & Testing

### 4.1 Functional Verification
- Integrated testing for GPS, LoraWAN communication, etc.

### 4.2 Performance Testing
- Battery lifespan testing.
- Performance evaluation under different conditions.

## 5. Conclusion & Future Directions
Analyze successes and challenges. Discuss future improvements and potential applications.

## 6. Appendices
Source codes, circuit diagrams, and technical documents.


# Pin out (LilyGO LORA32)
* I2S Speaker & Mic: SCK/BCK_PIN =4, WS/LCK_PIN =25, SD/DIN_PIN =0, MIC_SD=12
* I2C: SDA =21, SCL =22
* SDCARD: slot=3 (sck=14, mosi=15, miso=2, cs=13)
* LORA: MOSI=27, SCLK=5, CS=18, DIO=26, RST=23, MISO=19
* GPS: TX=14, RX=34
* Button: 35
* Unused pins :36,39
