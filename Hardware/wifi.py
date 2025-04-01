import os
import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

import oled
import main

def check_wifi():
    ssid = os.popen("iwgetid -r").read().strip()
    return ssid if ssid else None

def connectivity():
    ssid = check_wifi()
    if ssid:
        return True

    else:
        #message = "Connect your wifi..!"
        return False

if __name__ == "__main__":
    while True:
        if connectivity():
            oled.display("Wifi connected")
            main.run()

        else:
            oled.display("Wifi Not connected")
        time.sleep(5)