import cv
import time
import lockScreen
from faceRecognition import *

WINDOW_NAME = "window"

# TODO make it a user flag that defaults to 5 second
TIME_UNTIL_LOCK = 5

def getCameraIndex():
  for i in xrange(5):
    capture = cv.CaptureFromCAM(i)
    if capture:
      return i

WEBCAM_NR = getCameraIndex()
cv.NamedWindow(WINDOW_NAME, cv.CV_WINDOW_AUTOSIZE)
capture = cv.CaptureFromCAM(WEBCAM_NR)

lastTimeDetected = time.time()
while True:
  frame = cv.QueryFrame(capture)
  # TODO make this a flag, to see if user wants to see the webcam
  # either with recognized set or without
  cv.ShowImage(WINDOW_NAME, frame)
  faces = getFaces(frame)
  if faces:
    lastTimeDetected = time.time()
    print "found face"
    for f in faces:
      print f
  else:
    if (time.time() - lastTimeDetected > TIME_UNTIL_LOCK):
      print "no face found, locking screen"
      lockScreen.lockScreen()
  drawFaces(faces, frame)
  cv.SaveImage("withDetected.jpg", frame)
  cv.WaitKey(10)
  # time.sleep(0.5)



