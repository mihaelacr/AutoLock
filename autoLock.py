import argparse
import cv2
import signal
import sys
import time

from faceRecognition import *
import ignoreoutput
import system


DEFAULT_TIME_UNTIL_LOCK = 10
WINDOW_NAME = "AutoLock"
TIME_BETWEEN_FACE_CHECKS = 0.1
TIME_BETWEEN_LOCKS = 100
SLEEP_TIME_WHEN_NOT_CHARGING = 600  # 10 minutes

parser = argparse.ArgumentParser(description=("Automatically lock your screen "
                                              "when not inin range"))
parser.add_argument('--displayWebcam', action='store_const', const=True,
                    help="determies if the image from the webcam is displayed")
parser.add_argument("--runWithDischargingBattery", action='store_const', const=True,
                    help=("if this flag is specified, the program will run even"
                          "when the battery is discharging"))
parser.add_argument("--seeFaces", action='store_const', const=True,
                    help=("If passed as argument, the webcam image will show the "
                          "detected faces. Note that this automatically ensures "
                          "that the camera will be displayed."))
parser.add_argument("--myFace", action="store_const", const=True,
                     help=("If true, only recognizes the face of the person initially"
                            "sitting in front of the computer.")
parser.add_argument("-timeUntilLock", type=int, default=DEFAULT_TIME_UNTIL_LOCK,
                    help=("Time in seconds since the last time a face is detected"
                          "to the time the screen is locked. "
                          "Default value %d seconds." %DEFAULT_TIME_UNTIL_LOCK))
parser.add_argument("-frequency", type=float, default=TIME_BETWEEN_FACE_CHECKS,
                    help=("Time in seconds between face checks. Note that a small"
                          "number increases CPU usage but gives more accuracy."
                          "A big number might imply that the screen locks, "
                          "even though you are in front of the computer. "
                          "Default value %f seconds" %TIME_BETWEEN_FACE_CHECKS))
parser.add_argument("-minTimeBetweenLocks", type=float, default=TIME_BETWEEN_LOCKS,
                    help=("Minimal time in seconds between screen locks."
                          "Default value %f seconds" %TIME_BETWEEN_LOCKS))


args = parser.parse_args()
displayCam = args.displayWebcam
runWithDischargingBattery = args.runWithDischargingBattery
timeUntilLock = args.timeUntilLock
frequency = args.frequency
minTimeBetweenLocks = args.minTimeBetweenLocks
displayFaces = args.seeFaces
oneFace  = args.myFace

# When user presses Control-C, gracefully exit program
def signal_handler(signal, frame):
  print "AutoLock will terminate."
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def getCameraCapture():
  with ignoreoutput.suppress_stdout_stderr():
  # 0 is supposed to detected any webcam connected to the device
    return cv2.VideoCapture(0)


def showFrame(frame, faces, draw=False):
  if draw:
    drawFaces(frame, faces)
  cv2.imshow(WINDOW_NAME, frame)
  cv2.waitKey(100)


# Currently does not destroy window due to OpenCV issues
def destroyWindow():
  cv2.destroyWindow(WINDOW_NAME)
  cv2.waitKey(1)

# Draw faces argument is only taken into account if display was set as true.
def detectedAndDisplayFaces(capture, display=False, drawFaces=False):
  flag, frame = capture.read()
  # Not sure if there is an error from the cam if we should lock the screen
  if flag:
    faces = getFaces(frame)
    if display:
      showFrame(frame, faces, drawFaces)
    if faces:
      return True
  else:
    return True


# Draw faces argument is only taken into account if display was set as true.
def oneCycleFaceDetection(lastTimeLocked, frequency,
                          display=False, drawFaces=False):
  capture = getCameraCapture()
  currentTime = time.time()
  lastTimeDetected = currentTime
  batteryDischarging = -1

  while currentTime - lastTimeDetected < timeUntilLock:
    currentTime = time.time()
    if not runWithDischargingBattery:
      if not system.isCharging():
        if batteryDischarging > 0:
          if currentTime - batteryDischarging > timeUntilLock:
            break
        else:
          batteryDischarging = currentTime
      else:
        batteryDischarging = -1

    if detectedAndDisplayFaces(capture, display, drawFaces):
      lastTimeDetected = currentTime

    time.sleep(frequency)

  if currentTime - lastTimeLocked > minTimeBetweenLocks:
    system.lockScreen()

  return lastTimeLocked


def lockWhenFaceNotDetected(timeUntilLock, frequency, display=False, drawFaces=False):
  lastTimeLocked = time.time() - minTimeBetweenLocks

  if display:
    cv2.startWindowThread()
    cv2.namedWindow(WINDOW_NAME, cv2.CV_WINDOW_AUTOSIZE)

  while True:
    # Unless the user specified otherwise, do not run while machine is not
    # not charging
    if not runWithDischargingBattery:
      if display and not system.isCharging():
        destroyWindow()
      while not system.isCharging():
        time.sleep(SLEEP_TIME_WHEN_NOT_CHARGING)

    lastTimeLocked = oneCycleFaceDetection(lastTimeLocked, frequency, display, drawFaces)


def main():
  global timeUntilLock
  global frequency
  if frequency >= timeUntilLock:
    print ("The time between face detection checks is bigger than the time "
           "until lock. This would result in locking the screen regardless "
           "of someone's presence in front of the screen.")
    print ("As a consequence, defaulting the time between face checks "
           "to half of the time until the screen is locked when no face is detected.")
    frequency = timeUntilLock / 2

  if displayFaces:
    showCam = True
  else:
    showCam = displayCam

  if system.isCharging() or runWithDischargingBattery:
    if runWithDischargingBattery:
      print "You chose to run AutoLock with your laptop not plugged in"
      print "Be aware of your battery"
    if timeUntilLock < 1:
      print ("timeUntilLock has to be a positive integer, as it represents"
             "the number of seconds since a face was detected to the time the "
             "screen gets locked")
      print "Defaulting to %d seconds" %(DEFAULT_TIME_UNTIL_LOCK)
      timeUntilLock = DEFAULT_TIME_UNTIL_LOCK
    lockWhenFaceNotDetected(timeUntilLock, frequency, showCam, displayFaces)
  else:
    print "Your machine is not charging, AutoLock will not execute"


if __name__ == '__main__':
  main()
