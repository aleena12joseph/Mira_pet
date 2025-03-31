# Mira Setup Guide

## 1. Hardware Requirements

- **Raspberry Pi 4** (or higher)
- **3 Servo Motors** (for movement)
- **OLED Display**
- **DHT11 Sensors** (for humidity and temperature)
- **Motor Driver**
- **LED**
- **Microphone and Speaker**

## 2. Software Requirements

- **Python 3.8+**
- **Git**
- **Raspberry Pi OS** installed
- **API Keys** (listed below)
- **Required Libraries** (listed below)

### 2.1 API Keys

- **Google Cloud TTS API Key**
- **Gemini AI API Key**
- **Google weather API**

### 2.2 Required Libraries

- `google-generativeai`
- `datetime`
- `requests`
- `base64`
- `pygame`
- `speech_recognition`
- `pyttsx3`

## 3. Tools

- **Breadboard** and **jumper wires**
- **Soldering kit** (if necessary)

## 4. Raspberry Pi Setup

### 4.1 Install Raspberry Pi OS

1. Use **Raspberry Pi Imager** to install **Raspberry Pi OS**.
2. Insert the SD card into the Raspberry Pi and boot it up.

### 4.2 Initial Configuration

1. Complete the setup (Wi-Fi, timezone, etc.).
2. Open Terminal and update your Pi:
    ```bash
    sudo apt update
    sudo apt upgrade
    ```

### 4.3 Enable I2C and GPIO

1. Open the configuration tool:
    ```bash
    sudo raspi-config
    ```
2. Enable I2C and GPIO:
   - Go to **Interfacing Options > I2C** and enable it.
   - Enable **GPIO** for controlling servos.
3. Reboot the Pi.

## 5. Set Up API Keys

### 5.1 Google Cloud API (Text-to-Speech)

1. Go to the **Google Cloud Console**.
2. Create a new project and enable the **Text-to-Speech API**.
3. Create credentials (API key) and download the key.
4. Paste the API key in your `YOUR_GOOGLE_CLOUD_API_KEY` variable in your Python code.

### 5.2 Gemini AI API

1. Sign up and create a project on **Gemini AI** (or your chosen AI provider).
2. Obtain the **API key** for Gemini.
3. Paste the API key in your `YOUR_GEMINI_API_KEY` variable in the Python code.

### 5.3 Weather API

1. Sign up for an **API key** from a weather provider like **OpenWeather** or **WeatherStack**.
2. Store the API key in your code for fetching weather data.

## 6. Hardware Setup

1. **Connect Devices**:
   - **OLED Display (I2C)**: Connect it to the corresponding I2C pins on the Raspberry Pi.
   - **Servo Motors**: Connect to the GPIO pins.
   - **DHT11 Sensors**: Connect to the GPIO pins.
   - **LED**: Connect to the GPIO pins.
   - **Microphone**: Plug into the Raspberry Pi’s USB port.
   - **Speaker**: Connect to the Raspberry Pi’s audio port.

2. Ensure all components are securely connected and powered correctly.

## 7. Test Mira

1. Once everything is set up, run the script:
    ```bash
    python mira.py
    ```

2. Activate Mira:
   - Say "**Hey Mira!**" or "**Hi Mira!**" to trigger it.

3. Test commands like:
   - **"What’s the time?"**
   - **"Set alarm to 07:00."**
   - **"Respect at 75%."**

4. Mira will respond via the speaker and show emotions on the OLED display.

