import cv2

width = 640
height = 480

def init(w, h):
  global width, height
  width = w
  height = h

def resize(img):
  return cv2.resize(img, (width, height), interpolation = cv2.INTER_CUBIC)

def show(img):
  img = resize(img)
  cv2.imshow('display', img)
