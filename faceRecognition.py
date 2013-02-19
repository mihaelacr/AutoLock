import cv

imageName = "ela.jpg"
image = cv.LoadImage(imageName)

# Create window for image display
windowName = "openCVwindow"


def getFaces(image):
  storage = cv.CreateMemStorage()
  haar=cv.Load('haarcascade_frontalface_default.xml')

  #  A list of all faces detected in the picture
  # A face is represented by a rectange (x, y, w, h) and (strongness of face)
  detectedFaces = cv.HaarDetectObjects(image, haar, storage, 1.2, 2,cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
  return detectedFaces

def drawFaces(faces, image):
  # n is the number of neighbours which are used to create the face
  for (x, y, w, h), n in faces:
    cv.Rectangle(image, (x,y), (x + w, y + h), cv.RGB(255, 0, 0), thickness=5)

def getAndDisplayFaces(windowName, image, waitingTime=1000):
  cv.NamedWindow(windowName, cv.CV_WINDOW_AUTOSIZE)
  faces = getFaces(image)
  drawFaces(faces, image)
  cv.ShowImage(windowName, image)
  cv.WaitKey(waitingTime)
  cv.SaveImage("withDetected.jpg", image)

if __name__ == '__main__':
  getAndDisplayFaces(windowName, image)
