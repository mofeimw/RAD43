import cameraThreads
import motorControls

from picamera import PiCamera
from time import sleep
import signal
import RPi.GPIO as GPIO

from gpiozero import InputDevice, OutputDevice, PWMOutputDevice

def cleanup(signum, frame):
    motorControls.vibrate(PIN, False)
    GPIO.cleanup()
    exit()
signal.signal(signal.SIGINT, cleanup)

PIN = 16
motorControls.setUp(PIN)

cameraThreads.stream(PIN)
