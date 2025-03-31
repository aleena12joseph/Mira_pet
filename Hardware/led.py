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

if __name__ == "__main__":
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
