import cv2
import numpy as np
from pylab import *
from matplotlib import *
from matplotlib.pyplot import *
from scipy import *
import math

# to homogeneus coordinates
def toHom(points):
    N = len(points)
    hom = zeros((3, N))
    for i in range(N):
        (x, y) = points[i]
        hom[0][i] = x
        hom[1][i] = y
        hom[2][i] = 1
    return hom


def H_from_points(fp, tp):
    """ Find homography H, such that fp is mapped to tp
    using the linear DLT method. Points are conditioned automatically. """
    if fp.shape != tp.shape:
        raise RuntimeError('number of points do not match')

    # condition points (important for numerical reasons)

    #--from points
    m = mean(fp[:2], axis=1)
    maxstd = max(std(fp[:2], axis=1)) + 1e-9
    T1 = diag([1 / maxstd, 1 / maxstd, 1])
    T1[0][2] = -m[0] / maxstd
    T1[1][2] = -m[1] / maxstd
    fp = dot(T1, fp)

    # --to points--
    m = mean(tp[:2], axis=1)
    maxstd = max(std(tp[:2], axis=1)) + 1e-9
    T2 = diag([1 / maxstd, 1 / maxstd, 1])
    T2[0][2] = -m[0] / maxstd
    T2[1][2] = -m[1] / maxstd
    tp = dot(T2, tp)

    # create matrix for linear method, 2 rows for each correspondence pair
    nbr_correspondences = fp.shape[1]
    A = zeros((2 * nbr_correspondences, 9))
    for i in range(nbr_correspondences):
        A[2 * i] = [-fp[0][i], -fp[1][i], -1, 0, 0, 0, tp[0][i] * fp[0][i], tp[0][i] * fp            [1][i], tp[0][i]]
        A[2 * i + 1] = [0, 0, 0, -fp[0][i], -fp[1][i], -1, tp[1][i] * fp[0][i], tp[1][i] * fp              [1][i], tp[1][i]]

    U, S, V = linalg.svd(A)
    H = V[8].reshape((3, 3))

    # decondition
    H = dot(linalg.inv(T2), dot(H, T1)) # normalize and return
    return H / H[2, 2]


def mapPoint(H, (x, y)):
    p = zeros((3, 1))
    p[0][0] = x
    p[1][0] = y
    p[2][0] = 1.0

    p = dot(H, p)
    p = p / p[2][0]
    return (p[0][0], p[1][0])


def get_H(I):
  h, w = I.shape[:2]
  fp = [(0, 0), (w, 0), (0, h), (w, h)]
  tp = getMousePoints(I, 4)
  return H_from_points(toHom(fp), toHom(tp))


def getMousePoints(I, N):
    fig = figure(1)
    gray()
    imshow(I)
    draw()

    fig.hold('on')
    points = ginput(N)

    for (x, y) in points:
        plt.plot(x, y)

    show(False)
    return points


def forwardmap(I, H):
  h, w = I.shape[:2]

  proj = zeros(I.shape)
  for i in range(h):
    for j in range(w):
      x, y = mapPoint(H, (j, i))
      if x >= 0 and x <= w and y >= 0 and y <= h:
        proj[y, x] = I[i, j]

  gray = proj.astype('uint8')
  return gray

def backmap(I, H):
  h, w = I.shape[:2]

  proj = zeros(I.shape)
  for i in range(h):
      for j in range(w):
          x, y = mapPoint(H, (j, i))
          if x >= 0 and x <= w and y >= 0 and y <= h:
              # Nearest neighbor
              proj[i, j] = I[y, x]
              # TODO: interpolation

  gray = proj.astype('uint8')
  return gray
