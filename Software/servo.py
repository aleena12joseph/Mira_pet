import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import random

i2c = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c)
pca.frequency = 50

servoH = servo.Servo(pca.channels[0])
servoL = servo.Servo(pca.channels[1])
servoR = servo.Servo(pca.channels[2])

# Ensure servos have default positions to prevent NoneType errors
servoH.angle = 80
servoL.angle = 180
servoR.angle = 0

def init():
    for angle in range(int(servoH.angle or 80), 81, 10 if (servoH.angle or 80) < 80 else -10):
        servoH.angle = angle
        time.sleep(0.02)

    for angle in range(int(servoL.angle or 180), 181, 10 if (servoL.angle or 180) < 180 else -10):
        servoL.angle = angle
        time.sleep(0.02)

    for angle in range(int(servoR.angle or 0), 1, 10 if (servoR.angle or 0) < 0 else -10):
        servoR.angle = angle
        time.sleep(0.02)

def light(choice):
    if choice:
        for angle in range(int(servoL.angle or 180), 30, -10):
            servoL.angle = angle
            time.sleep(0.02)
    else:
        for angle in range(int(servoL.angle or 180), 181, 10):
            servoL.angle = angle
            time.sleep(0.02)

def move_servo_randomly(servo_obj, min_angle=30, max_angle=150, delay=1.5):
    current_angle = servo_obj.angle or 90  # Default if None
    target_angle = random.randint(min_angle, max_angle)
    step = 1 if target_angle > current_angle else -1

    for angle in range(int(current_angle), target_angle + 1, step):
        servo_obj.angle = angle
        time.sleep(0.02)

    time.sleep(delay)

def idle():
    try:
        move_servo_randomly(servoL, min_angle=150, max_angle=180, delay=0)
        move_servo_randomly(servoR, min_angle=0, max_angle=30, delay=0)
        move_servo_randomly(servoH, min_angle=60, max_angle=90, delay=4)
    except KeyboardInterrupt:
        print("\nStopping idle mode...")

def move(angleL, angleR, angleH, steps):
    servoH.angle = angleH
    for i in range(0, max(angleL, angleR) + 1, steps):
        if 180 - i >= angleL:
            servoL.angle = 180 - i
        if i <= angleR:
            servoR.angle = i
        time.sleep(0.02)
    servoH.angle = 80

def happy():
    move(130, 80, 60, 10)
    init()

def sad():
    move(170, 30, 90, 10)
    init()

def anger():
    move(0, 180, 80, 10)
    move(180, 0, 100, 20)
    init()

def love():
    move(90, 90, 60, 20)
    time.sleep(1)
    init()

def neutral():
    move(160, 0, 80, 10)
    time.sleep(2)
    init()

def test():
    for angle in range(0, 180, 10):
        if 0 <= angle <= 110:
            servoH.angle = angle
        servoL.angle = 180 - angle
        servoR.angle = angle
        time.sleep(0.02)

    for angle in range(180, 0, -10):
        if 0 <= angle <= 110:
            servoH.angle = angle
        servoL.angle = 180 - angle
        servoR.angle = angle
        time.sleep(0.02)

if _name_ == "_main_":
    try:
        init()
        neutral()
        init()
    except KeyboardInterrupt:
        print("\nStopping...")
        servoH.angle = 80
        servoL.angle = 180
        servoR.angle = 0
        pca.deinit()