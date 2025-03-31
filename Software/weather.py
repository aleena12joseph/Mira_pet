import time
import network
import urequests
import json

API_URL = "https://api.open-meteo.com/v1/forecast"
LAT = 28.6139  # Example: Latitude for Delhi
LON = 77.2090  # Example: Longitude for Delhi

# Wi-Fi credentials
SSID = ""  # Replace with your Wi-Fi SSID
PASSWORD = ""  # Replace with your Wi-Fi password

def check_wifi_connection():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
        print("Wi-Fi connected:", wlan.ifconfig())
    else:
        print("Wi-Fi is already connected:", wlan.ifconfig())

def format_time(timestamp):
    return "{:02d}-{:02d}-{:04d} {:02d}:{:02d}:{:02d}".format(
        timestamp[2], timestamp[1], timestamp[0],  # Day, Month, Year
        timestamp[3], timestamp[4], timestamp[5]   # Hour, Minute, Second
    )

def get_current_weather_from_api():
    # Ensure Wi-Fi is connected
    check_wifi_connection()

    try:
        # Construct API URL with parameters (latitude, longitude)
        api_url = f"{API_URL}?latitude={LAT}&longitude={LON}&hourly=temperature_2m"
        print(f"Fetching weather data from API: {api_url}")
        
        response = urequests.get(api_url)
        
        # Check if response is successful
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            return None
        
        data = response.json()
        
        # Extract the current temperature data
        hourly_data = data.get('hourly', {}).get('temperature_2m', [])
        
        if hourly_data:
            current_temperature = hourly_data[0]  # Assuming the first data point is the current time
            print(f"Current Temperature: {current_temperature}°C")
        else:
            print("No hourly temperature data available.")
        
        # Get current time and date
        current_time = time.localtime()
        formatted_time = format_time(current_time)
        
        print(f"Current Date and Time: {formatted_time}")
        
    except Exception as e:
        print("Failed to fetch current weather:", str(e))

# Driver code
if name == "main":
    get_current_weather_from_api()