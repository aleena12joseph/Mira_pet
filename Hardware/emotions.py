import time
import oled
import servo
import random

def emotions(emotion):
    if emotion == "Happiness":
        servo.happy()
        oled.happy()
    elif emotion == "Neutral":
        servo.neutral()
        oled.neutral()
    elif emotion == "Confused":
        #servo.confused()
        oled.confused()
    elif emotion == "Sadness":
        servo.sad()
        oled.sad()
    elif emotion == "Anger":
        servo.anger()
        oled.angry()
    elif emotion == "Love":
        servo.love()
        oled.love()
    elif emotion == "Blink":
        oled.blink()
    elif emotion == "idle":
        choice = random.randint(0,11)
        if choice == 6:
            emotions("Sadness")
        elif choice == 8:
            emotions("Happiness")
        else:
            servo.idle()

def test():
    oled.happy()
    servo.happy()
    time.sleep(2)

    oled.neutral()
    servo.neutral()
    time.sleep(2)

    oled.confused()
    #servo.confused()
    time.sleep(2)

    oled.sad()
    servo.sad()
    time.sleep(2)

    oled.angry()
    servo.anger()
    time.sleep(2)

    oled.love()
    servo.love()
    time.sleep(2)

    oled.blink()
    time.sleep(2)

if __name__ == "__main__":
    test()