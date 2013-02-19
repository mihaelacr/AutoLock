import argparse
import cv
import time

from faceRecognition import *
import lockScreen


DEFAULT_TIME_UNTIL_LOCK = 5

parser = argparse.ArgumentParser(description=("Automatically lock your screen when not in"
                                              "in range"))
parser.add_argument("-timeUntilLock", type=int, default=DEFAULT_TIME_UNTIL_LOCK,
                      help=("time in seconds since the last time a face is detected"
                           "to the time the screen is locked"))
parser.add_argument("--displayWebcam",
                      help="determies if the image from the webcam is displayed")


WINDOW_NAME = "window"

args = parser.parse_args()
display = args.displayWebcam
timeUntilLock = args.timeUntilLock

def getCameraIndex():
  for i in xrange(5):
    capture = cv.CaptureFromCAM(i)
    if capture:
      return i


# TODO clean up this if display which appears twice

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
    print "found face"
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
