import cv2 as cv
from picamera import PiCamera
from picamera.array import PiRGBArray
from ultralytics import YOLO

import motorControls

import time

def stream(MOTOR_PIN):
    # set up pi camera
    cam = PiCamera()
    cam.resolution = (512, 304)
    cam.framerate = 20
    rawCapture = PiRGBArray(cam, size=(512, 304))

    # load YOLO model
    model = YOLO('model.pt')

    while True:
        for frame in cam.capture_continuous(rawCapture, format='bgr', use_video_port=True):
            # grab frame and run model
            imageFrame = frame.array
            detections = model(imageFrame)[0]

            # loop through detections
            for data in detections.boxes.data.tolist():
                print(data)

                # discard if confidence under 25%
                confidence = data[4]
                if float(confidence) < 0.25:
                    continue

                # extract dimensions and perform calculations
                xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
                pixel_width = xmax - xmin
                real_width = 16 # inches
                # focal = (pixel_width x distance) / real_width
                focal = 100
                distance = (real_width * focal) / pixel_width

                # classify as walk or stop signal
                signal = data[5]
                if float(signal) == 1.0:
                    label = "walk"
                    color = (0, 240, 0) # walk => green
                    motorControls.vibrateLong(MOTOR_PIN) # signal motor
                else:
                    label = "stop"
                    color = (0, 0, 240) # stop => red
                    motorControls.doubleVibrate(MOTOR_PIN) # signal motor

                # add confidence and distance to label
                label += " [" + str(confidence)[:4] + "]"
                label += " ~" + str(distance)[:4] + "in"

                # draw box and label
                imageFrame = cv.rectangle(imageFrame, (xmin, ymin), (xmax, ymax), color, 6)
                cv.putText(imageFrame, label, (xmin, ymin - 10), cv.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)

            # render frame
            cv.imshow('stride', imageFrame)
            cv.waitKey(1)
