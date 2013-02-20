import argparse
import cv
import signal
import sys
import time


from faceRecognition import *
import batteryStatus
import ignoreoutput
import lockScreen


DEFAULT_TIME_UNTIL_LOCK = 5
WINDOW_NAME = "AutoLock"
TIME_BETWEEN_FACE_CHECKS = 1

parser = argparse.ArgumentParser(description=("Automatically lock your screen "
                                              "when not inin range"))
parser.add_argument("-timeUntilLock", type=int, default=DEFAULT_TIME_UNTIL_LOCK,
                      help=("time in seconds since the last time a face is detected"
                           "to the time the screen is locked"))
parser.add_argument("--displayWebcam",
                      help="determies if the image from the webcam is displayed")
parser.add_argument("--runWithDischargingBattery",
                      help=("if this flag is specified, the program will run even"
                            "when the battery is discharging"))


args = parser.parse_args()
displayCam = args.displayWebcam
timeUntilLock = args.timeUntilLock
runWithDischargingBattery = args.runWithDischargingBattery


# When user presses Control-C, gracefully exit program, without
def signal_handler(signal, frame):
  print 'You pressed Ctrl+C!'
  print "AutoLock will terminate."
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



def getCameraCapture():
  # -1 is supposed to detected any webcam connected to the device
  return cv.CaptureFromCAM(-1)


def lockWhenFaceNotDetected(timeUntilLock, display=False):
  if display:
    cv.NamedWindow(WINDOW_NAME, cv.CV_WINDOW_AUTOSIZE)

  capture = getCameraCapture()
  lastTimeDetected = time.time()
  lastTimeChecked = time.time()

  while True:
    # Unless the user specified otherwise, do not record while machine is not
    # not charging
    if not runWithDischargingBattery:
      while not batteryStatus.isCharging():
        pass
    currentTime = time.time()
    if (currentTime - lastTimeChecked > TIME_BETWEEN_FACE_CHECKS):
      frame = cv.QueryFrame(capture)
      if display:
        cv.ShowImage(WINDOW_NAME, frame)
        if cv.WaitKey(5) == 27:
          break
      faces = getFaces(frame)
      if faces:
        lastTimeDetected = currentTime
      else:
        if (time.time() - lastTimeDetected > timeUntilLock):
          print "no face found, locking screen"
          lockScreen.lockScreen()
      drawFaces(faces, frame)


def main():
  global timeUntilLock
  if batteryStatus.isCharging() or runWithDischargingBattery:
    if runWithDischargingBattery:
      print "You choose to run AutoLock with your laptop not plugged in"
      print "Be aware of your battery"
    if timeUntilLock < 1:
      print ("timeUntilLock has to be a positive integer, as it represents"
             "the number of seconds since a face was detected to the time the "
             "screen gets locked")
      print "Defaulting to %d seconds" %(DEFAULT_TIME_UNTIL_LOCK)
      timeUntilLock = DEFAULT_TIME_UNTIL_LOCK
    lockWhenFaceNotDetected(timeUntilLock, displayCam)
  else:
    print "Your machine is not charging, AutoLock will not execute"

if __name__ == '__main__':
  main()
