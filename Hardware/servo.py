import RPi.GPIO as GPIO
import time

import servo

LED_PIN = 17  # GPIO 17 (Pin 11)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def lights():
    led_status = GPIO.input(LED_PIN)
    if led_status == GPIO.HIGH:
        servo.light(0)
        GPIO.output(LED_PIN, GPIO.LOW)
        return 0
    else:
        servo.light(1)
        GPIO.output(LED_PIN, GPIO.HIGH)
        return 1

if _name_ == "_main_":
    try:
        while True:
            GPIO.output(LED_PIN, GPIO.HIGH)  # LED ON
            time.sleep(1)  # Wait 1 second
            GPIO.output(LED_PIN, GPIO.LOW)  # LED OFF
            time.sleep(1)  # Wait 1 second

    except KeyboardInterrupt:
        print("Stopped by user")

    finally:
        GPIO.cleanup()  # Clean up GPIO
        import adafruit_dht
import time
import board

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

            if temperature > 40.0:
                print("⚠ Temperature too high!")
                return 1
            else: return 0

        else:
            print("Failed to read sensor. Retrying...")
    except RuntimeError:
        return False  # Assume safe temperature if reading fails

if _name_ == "_main_":
    try:
        while True:
            try:
                temperature = dht_device.temperature
                humidity = dht_device.humidity

                if temperature is not None and humidity is not None:
                    print(f"Temperature: {temperature}°C")
                    print(f"Humidity: {humidity}%")

                    if temperature > 40.0:
                        print("⚠ Temperature too high!")

                else:
                    print("Failed to read sensor. Retrying...")

            except RuntimeError as e:
                print(f"Error reading DHT11: {e}")
                time.sleep(2)  # Short delay before retrying

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting gracefully. Cleaning up resources.")
        import random

def generate_number(lower, upper):
    return random.randint(lower, upper)

def get_user_guess():
    while True:
        guess = input("Enter your guess: ").strip()
        if guess.isdigit():
            return int(guess)
        print("Invalid input. Please enter a valid number.")

def check_guess(guess, target):
    if guess < target:
        return "Too low!"
    elif guess > target:
        return "Too high!"
    else:
        return "Correct!"

def play_game():
    lower, upper = 1, 10
    target = generate_number(lower, upper)
    print("Guess a number between 1 and 10:")
    while True:
        guess = get_user_guess()
        result = check_guess(guess, target)
        print(result)
        if result == "Correct!":
            break

def main():
    while True:
        play_game()
        play_again = input("Play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            break

if _name_ == "_main_":
    main()