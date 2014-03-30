import cv2

import homography as hom

width = 640
height = 480
H = None

def init(w, h):
  global width, height
  width = w
  height = h

def set_H(h):
  global H
  H = h

def resize(img):
  return cv2.resize(img, (width, height), interpolation = cv2.INTER_CUBIC)

def show(img):
  if H != None:
    img = hom.forwardmap(img, H)

  img = resize(img)
  cv2.imshow('display', img)
