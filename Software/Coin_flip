import time
import board
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306
import random
import pygame

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("./Music/super_mario.wav")

def coin_flip():
    pygame.mixer.music.play()
    for _ in range(10):
        image = Image.open("./Emotions/Head_or_Tails/Head.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
        time.sleep(0.05)

        image = Image.open("./Emotions/Head_or_Tails/Tail.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
        time.sleep(0.05)
    result = random.choice(["Heads", "Tails"])

    if result == "Heads":
        image = Image.open("./Emotions/Head_or_Tails/Head.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
    else:
        image = Image.open("./Emotions/Head_or_Tails/Tail.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
    return result

if __name__ == "__main__":
    try:
        print("Coin Flip Result:", coin_flip())
        image = Image.open("./Emotions/Idle/Normal.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
    except KeyboardInterrupt:
        print("Stopped")
        image = Image.open("./Emotions/Idle/Normal.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
