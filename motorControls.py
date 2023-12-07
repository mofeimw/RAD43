from time import sleep
import RPi.GPIO as GPIO

def setUp(MOTOR_PIN):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_PIN, GPIO.OUT)

def vibrate(MOTOR_PIN, control):
    if control:
        GPIO.output(MOTOR_PIN, GPIO.HIGH)
        print("vibrating!!!")
    else:
        GPIO.output(MOTOR_PIN, 0)
        print("not vibrating.")

def vibrateLong(MOTOR_PIN):
    vibrate(MOTOR_PIN, True)
    sleep(3)
    vibrate(MOTOR_PIN, False)

def doubleVibrate(MOTOR_PIN):
    vibrate(MOTOR_PIN, True)
    sleep(0.5)
    vibrate(MOTOR_PIN, False)
    sleep(0.2)
    vibrate(MOTOR_PIN, True)
    sleep(0.5)
    vibrate(MOTOR_PIN, False)
