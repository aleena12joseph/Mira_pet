import adafruit_dht
import time
import board

import oled

# Initialize DHT11 sensor on GPIO 17
dht_device = adafruit_dht.DHT11(board.D17)

def check_temp():
    """Checks if the temperature exceeds 40°C."""
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")

            if temperature > 33.0:
                print("⚠️ Temperature too high!")
                oled.display(f"Temp: {temperature:.2f} C")
                return 1
            else: return 0

        else:
            print("Failed to read sensor. Retrying...")
    except RuntimeError:
        return False  # Assume safe temperature if reading fails

if __name__ == "__main__":
    try:
        while True:
            try:
                temperature = dht_device.temperature
                humidity = dht_device.humidity

                if temperature is not None and humidity is not None:
                    print(f"Temperature: {temperature}°C")
                    print(f"Humidity: {humidity}%")

                    if temperature > 40.0:
                        print("⚠️ Temperature too high!")

                else:
                    print("Failed to read sensor. Retrying...")

            except RuntimeError as e:
                print(f"Error reading DHT11: {e}")
                time.sleep(2)  # Short delay before retrying

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting gracefully. Cleaning up resources.")