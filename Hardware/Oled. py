import time
import board
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

current_emotion = "Neutral"

def emotions(emotion):
    global current_emotion
    if emotion == "Happiness":
        current_emotion = "Happiness"
        happy()
    elif emotion == "Neutral":
        current_emotion = "Neutral"
        neutral()
    elif emotion == "Confused":
        current_emotion = "Confused"
        confused()
    elif emotion == "Sadness":
        current_emotion = "Sadness"
        sad()
    elif emotion == "Anger":
        current_emotion = "Anger"
        angry()
    elif emotion == "Love":
        current_emotion = "Love"
        love()
    elif emotion == "Blink":
        blink()

def test():
    for _ in range(2):
        neutral()
        time.sleep(2)

        image = Image.open("./Emotions/Idle/Left.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
        time.sleep(2)

        image = Image.open("./Emotions/Idle/Bottom-left.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
        time.sleep(2)

        image = Image.open("./Emotions/Idle/Top-left.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
        time.sleep(2)

        image = Image.open("./Emotions/Idle/Right.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
        time.sleep(2)

        image = Image.open("./Emotions/Idle/Bottom-right.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
        time.sleep(2)

        image = Image.open("./Emotions/Idle/Top-right.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
        time.sleep(2)

        happy()
        time.sleep(2)

        sad()
        time.sleep(2)

        angry()
        time.sleep(2)

        blink()
        time.sleep(2)

        confused()
        time.sleep(2)

        love()
        time.sleep(2)

        image = Image.open("./Emotions/Head_or_Tails/Head.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
        time.sleep(2)

        image = Image.open("./Emotions/Head_or_Tails/Tail.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
        time.sleep(2)

def happy():
    image = Image.open("./Emotions/Happy/Happy.png").convert("1")
    image = image.resize((128, 64))
    oled.image(image)
    oled.show()

def neutral():
    image = Image.open("./Emotions/Idle/Normal.png").convert("1")
    image = image.resize((128, 64))
    oled.image(image)
    oled.show()

def sleep():
    pass

def angry():
    image = Image.open("./Emotions/Angry/Angry.png").convert("1")
    image = image.resize((128, 64))
    oled.image(image)
    oled.show()

def sad():
    image = Image.open("./Emotions/Sad/Sad.png").convert("1")
    image = image.resize((128, 64))
    oled.image(image)
    oled.show()

def love():
    image = Image.open("./Emotions/Love/Love.png").convert("1")
    image = image.resize((128, 64))
    oled.image(image)
    oled.show()

def confused():
    image = Image.open("./Emotions/Confused/Confused.png").convert("1")
    image = image.resize((128, 64))
    oled.image(image)
    oled.show()

def blink():
    global current_emotion

    image = Image.open("./Emotions/Blink/Blink.png").convert("1")
    image = image.resize((128, 64))
    oled.image(image)
    oled.show()
    #time.sleep(0.02)

    if current_emotion == "Happiness":
        happy()
    elif current_emotion == "Neutral":
        neutral()
    elif current_emotion == "Confused":
        confused()
    elif current_emotion == "Sadness":
        sad()
    elif current_emotion == "Anger":
        angry()
    elif current_emotion == "Love":
        current_emotion = "Love"
        love()

if __name__ == "__main__":
    try:
        test()
        #for _ in range(10):
         #   blink()
          #  time.sleep(5)

    except KeyboardInterrupt:
        print("Stopped")
        image = Image.open("./Emotions/Idle/Normal.png").convert("1")
        image = image.resize((128, 64))
        oled.image(image)
        oled.show()
