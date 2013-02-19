import argparse
import cv
import time

from faceRecognition import *
import lockScreen
import batteryStatus

DEFAULT_TIME_UNTIL_LOCK = 5

parser = argparse.ArgumentParser(description=("Automatically lock your screen when not in"
                                              "in range"))
parser.add_argument("-timeUntilLock", type=int, default=DEFAULT_TIME_UNTIL_LOCK,
                      help=("time in seconds since the last time a face is detected"
                           "to the time the screen is locked"))
parser.add_argument("--displayWebcam",
                      help="determies if the image from the webcam is displayed")
parser.add_argument("--runWithDischargingBattery",
                      help=("if this flag is specified, the program will run even"
                            "when the battery is discharging"))


WINDOW_NAME = "AutoLock"

args = parser.parse_args()
displayCam = args.displayWebcam
timeUntilLock = args.timeUntilLock
runWithDischargingBattery = args.runWithDischargingBattery

def getCameraIndex():
  for i in xrange(5):
    capture = cv.CaptureFromCAM(i)
    if capture:
      return i


def lockWhenFaceNotDetected(display=False):
  if display:
    cv.NamedWindow(WINDOW_NAME, cv.CV_WINDOW_AUTOSIZE)
  capture = cv.CaptureFromCAM(getCameraIndex())

  lastTimeDetected = time.time()
  while True:
    frame = cv.QueryFrame(capture)
    if display:
      cv.ShowImage(WINDOW_NAME, frame)
    faces = getFaces(frame)
    if faces:
      lastTimeDetected = time.time()
      for f in faces:
        print f
    else:
      if (time.time() - lastTimeDetected > timeUntilLock):
        print "no face found, locking screen"
        lockScreen.lockScreen()
    drawFaces(faces, frame)
    cv.SaveImage("withDetected.jpg", frame)
    cv.WaitKey(10)
    # time.sleep(0.5)


def main():
  if batteryStatus.isCharging() or runWithDischargingBattery:
    if runWithDischargingBattery:
      print "You choose to run AutoLock with your laptop not plugged in"
      print "Be aware of your battery"
    lockWhenFaceNotDetected(displayCam)

if __name__ == '__main__':
  main()
