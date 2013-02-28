import cv2

# Create window for image display
CASCADE_FN = "haarcascade_frontalface_default.xml"

def getFaces(image):
  cascade = cv2.CascadeClassifier(CASCADE_FN)
  img_copy = cv2.resize(image, (image.shape[1]/2, image.shape[0]/2))
  gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
  gray = cv2.equalizeHist(gray)
  rects = cascade.detectMultiScale(gray)
  return list(rects)

def drawFaces(faces, image):
  for (x, y, w, h) in faces:
    cv2.rectangle(image, (x,y), (x + w, y + h), cv2.RGB(255, 0, 0), thickness=5)

def getAndDisplayFaces(windowName, image, waitingTime=1000):
  cv2.namedWindow(windowName, cv2.CV_WINDOW_AUTOSIZE)
  faces = getFaces(image)
  drawFaces(faces, image)
  cv2.imshow(windowName, image)
  cv2.waitKey(waitingTime)
  cv2.imsave("withDetected.jpg", image)
