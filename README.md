# Outdoor Guardian: An Embedded Solution for Outdoor Enthusiasts

## Introduction

**Background:**  
In today's fast-paced world, people increasingly turn to outdoor activities such as hiking, skiing, and mountaineering to rejuvenate and reconnect with nature. Safety and communication are paramount during these adventures, especially in challenging terrains and unpredictable conditions.

**Project Overview:**  
The Outdoor Guardian is an innovative embedded device designed for outdoor adventurers, providing long-range, low-power communication, real-time tracking, and heart rate monitoring for enhanced safety. This project was developed as part of an undergraduate capstone project in the Electrical Engineering and Computer Sciences department at the University of California, Berkeley.

## Features

- **Long-Range Communication**: Utilizes LoRaWAN technology for communication over distances up to 5km.
- **Real-Time GPS Tracking**: Offers real-time location tracking for navigation and safety.
- **Heart Rate Monitoring**: Integrated MAX30102 sensor for continuous heart rate monitoring.
- **Audio Output**: Features PCM5102 I2S Lossless DAC for clear audio communication.
- **Energy Efficiency**: Designed for low power consumption with an efficient power management system.

## Hardware Components

- Microcontroller: LilyGo-LoRa-ESP32
- Heart Rate Sensor: MAX30102
- Audio DAC: PCM5102 I2S Lossless
- GPS Module: GY-NEO6MV1/GY-NEO6MV2
- Additional: Various resistors, capacitors, and power supply components

### Pin out (LilyGO LORA32)
* I2S Speaker & Mic: SCK/BCK_PIN =4, WS/LCK_PIN =25, SD/DIN_PIN =0, MIC_SD=12
* I2C: SDA =21, SCL =22
* SDCARD: slot=3 (sck=14, mosi=15, miso=2, cs=13)
* LORA: MOSI=27, SCLK=5, CS=18, DIO=26, RST=23, MISO=19
* GPS: TX=14, RX=34
* Button: 35
* Unused pins :36,39


## Acknowledgments

Special thanks to our project advisors and the UC Berkeley EECS department for their support and guidance.



