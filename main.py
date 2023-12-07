import cameraThreads
import motorControls

from picamera import PiCamera
from time import sleep
import signal
import RPi.GPIO as GPIO

from gpiozero import InputDevice, OutputDevice, PWMOutputDevice

# clean up on interrupt
def cleanup(signum, frame):
    motorControls.vibrate(PIN, False)
    GPIO.cleanup()
    exit()
signal.signal(signal.SIGINT, cleanup)

# set up motor pin
PIN = 16
motorControls.setUp(PIN)

# start camera stream
cameraThreads.stream(PIN)
